from django.utils.translation import gettext_lazy as _

from zaida.utils import messages
from zaida.verification.models.base import Verification
from zaida.verification.models.managers import EmailVerificationManager


class EmailVerification(Verification):
    class Meta(Verification.Meta):
        verbose_name = _("email verification")
        verbose_name_plural = _("email verifications")

    objects = EmailVerificationManager()

    MESSAGES = messages.email_verification