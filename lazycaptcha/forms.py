"""Form mixin that wires the request IP into the captcha field."""

from __future__ import annotations

from lazycaptcha.fields import LazyCaptchaField


class LazyCaptchaFormMixin:
    """
    Mixin that forwards the request's client IP to any LazyCaptchaField.

    Usage::

        class ContactForm(LazyCaptchaFormMixin, forms.Form):
            email = forms.EmailField()
            message = forms.CharField()
            captcha = LazyCaptchaField()

        # In your view:
        form = ContactForm(request.POST, request=request)
    """

    def __init__(self, *args, request=None, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

        if request is not None:
            ip = _client_ip(request)
            for field in self.fields.values():
                if isinstance(field, LazyCaptchaField):
                    field._remote_ip = ip


def _client_ip(request) -> str:
    xff = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "") or ""
