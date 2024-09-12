from __future__ import annotations

from typing import Any

from django.utils import timezone

from rest_framework import exceptions, serializers

from drf_spectacular.utils import extend_schema_field

from asu.auth.serializers.user import UserPublicReadSerializer
from asu.messaging.models import Conversation, ConversationRequest, Event, Message


class MessageSerializer(serializers.ModelSerializer[Message]):
    source = serializers.SerializerMethodField()  # type: ignore[assignment]

    class Meta:
        model = Message
        fields = ("id", "body", "source", "reply_to_id")

    @extend_schema_field(serializers.ChoiceField(choices=["sent", "received"]))
    def get_source(self, message: Message) -> str:
        user = self.context["request"].user
        return "sent" if message.sender_id == user.pk else "received"


class MessageComposeSerializer(serializers.ModelSerializer[Event]):
    # todo make this polymorphic, cases: groupmsg, privmsg, groupjoin
    # todo: make a reusable helper that resolves polymorphic serialization
    # todo: polymorphic though event modelmethod
    content = MessageSerializer(read_only=True, source="message")

    body = serializers.CharField(write_only=True)
    reply_to_id = serializers.IntegerField(min_value=1, required=False, write_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "type",
            "content",
            "body",
            "reply_to_id",
            "conversation_id",
            "date_created",
        )
        extra_kwargs = {"type": {"read_only": True}}

    def create(self, validated_data: dict[str, Any]) -> Event:
        sender, recipient, body, reply_to_id = (
            self.context["request"].user,
            self.context["recipient"],
            validated_data["body"],
            validated_data.get("reply_to_id"),
        )
        event = Message.objects.compose(sender, recipient, body, reply_to_id)
        if event is None:
            raise exceptions.PermissionDenied
        return event


class EventSerializer(serializers.ModelSerializer[Event]):
    content = MessageSerializer(source="message")  # todo polymorphic
    # interactions field here

    class Meta:
        model = Event
        fields = ("id", "type", "content", "date_created")


class ConversationSerializer(serializers.HyperlinkedModelSerializer[Conversation]):
    target = UserPublicReadSerializer(
        fields=(
            "id",
            "display_name",
            "username",
            "profile_picture",
            "is_private",
            "url",
        ),
        ref_name="ConversationUserTarget",
    )
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = (
            "id",
            "target",
            "last_message",
            "date_created",
            "date_modified",
            "url",
        )
        extra_kwargs = {"url": {"view_name": "api:messaging:conversation-detail"}}

    @extend_schema_field(MessageSerializer(allow_null=True))
    def get_last_message(self, obj: Conversation) -> dict[str, Any] | None:
        if (msg := obj.last_message) is None:  # type: ignore[attr-defined]
            return None

        message = Message(**msg)
        serializer = MessageSerializer(message, context=self.context)
        return serializer.data


class ConversationDetailSerializer(ConversationSerializer):
    accept_required = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = (
            "id",
            "target",
            "accept_required",
            "last_message",
            "date_created",
            "date_modified",
            "url",
        )
        extra_kwargs = {"url": {"view_name": "api:messaging:conversation-detail"}}

    def get_accept_required(self, conversation: Conversation) -> bool:
        return ConversationRequest.objects.filter(
            date_accepted__isnull=True,
            recipient=conversation.holder_id,
            sender=conversation.target_id,
        ).exists()


class ReadConversationSerializer(serializers.Serializer[dict[str, Any]]):
    until = serializers.DateTimeField()
    affected = serializers.IntegerField(read_only=True, min_value=0)

    def create(self, validated_data: dict[str, Any]) -> dict[str, Any]:
        conversation = self.context["conversation"]
        read_by = self.context["request"].user

        until = validated_data["until"]
        affected = conversation.messages.filter(
            recipient=read_by,
            date_read__isnull=True,
            date_created__lte=until,
        ).update(date_read=timezone.now())
        return {"until": until, "affected": affected}
