"""Form field that auto-verifies the token on clean()."""

from __future__ import annotations

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from lazycaptcha.client import LazyCaptchaClient
from lazycaptcha.widgets import LazyCaptchaWidget


class LazyCaptchaField(forms.CharField):
    """
    Django form field that renders the LazyCaptcha widget and verifies the
    token against the LazyCaptcha API during form validation.

    The field requires a request to be attached to the form in order to
    forward the client IP. Two approaches:

        1. Pass ``request`` to form.__init__ and have your form retain it
        2. Use the LazyCaptchaFormMixin which does #1 for you
    """

    default_error_messages = {
        "missing": _("Please complete the CAPTCHA challenge."),
        "invalid": _("CAPTCHA verification failed. Please try again."),
    }

    widget = LazyCaptchaWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label", "")
        kwargs.setdefault("required", True)
        self.min_score: float | None = kwargs.pop("min_score", None)
        self._client: LazyCaptchaClient = kwargs.pop("client", None) or LazyCaptchaClient()
        super().__init__(*args, **kwargs)

    def validate(self, value):
        if not value:
            raise ValidationError(self.error_messages["missing"], code="missing")

    def clean(self, value):
        value = super().clean(value)
        # IP is injected via LazyCaptchaFormMixin; default to None otherwise.
        remote_ip = getattr(self, "_remote_ip", None)

        result = self._client.verify(value, remote_ip)
        if not result.get("success"):
            raise ValidationError(self.error_messages["invalid"], code="invalid")

        if self.min_score is not None:
            score = float(result.get("score") or 0.0)
            if score < self.min_score:
                raise ValidationError(
                    _("Captcha risk score too low: %(score)s"),
                    params={"score": score},
                    code="low_score",
                )
        return value
