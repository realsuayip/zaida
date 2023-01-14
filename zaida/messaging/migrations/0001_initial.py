# Generated by Django 4.0.1 on 2022-07-14 12:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("has_receipt", models.BooleanField(default=True)),
                (
                    "date_read",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="date read"
                    ),
                ),
                (
                    "date_modified",
                    models.DateTimeField(
                        auto_now=True, verbose_name="date modified"
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "message",
                "verbose_name_plural": "messages",
            },
        ),
        migrations.CreateModel(
            name="ConversationRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date_accepted",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="date_accepted"
                    ),
                ),
                (
                    "date_modified",
                    models.DateTimeField(
                        auto_now=True, verbose_name="date modified"
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "conversation request",
                "verbose_name_plural": "conversation requests",
            },
        ),
        migrations.CreateModel(
            name="Conversation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date_modified",
                    models.DateTimeField(
                        auto_now=True, verbose_name="date modified"
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date created"
                    ),
                ),
                (
                    "holder",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="conversations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "messages",
                    models.ManyToManyField(
                        related_name="conversations", to="messaging.Message"
                    ),
                ),
                (
                    "target",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="targeted_conversations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="conversationrequest",
            constraint=models.UniqueConstraint(
                fields=("sender", "recipient"),
                name="unique_conversation_request",
            ),
        ),
        migrations.AddConstraint(
            model_name="conversation",
            constraint=models.UniqueConstraint(
                fields=("holder", "target"), name="unique_conversation"
            ),
        ),
    ]