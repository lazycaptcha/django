"""Form widget that renders the LazyCaptcha embed."""

from __future__ import annotations

from django import forms
from django.utils.safestring import mark_safe

from lazycaptcha.conf import get_setting


class LazyCaptchaWidget(forms.Widget):
    """Renders the LazyCaptcha widget div and ensures the script is included."""

    template_name = "lazycaptcha/widget.html"

    def __init__(
        self,
        attrs: dict | None = None,
        site_key: str | None = None,
        type: str | None = None,
        theme: str | None = None,
    ):
        super().__init__(attrs)
        self.site_key = site_key
        self.type = type
        self.theme = theme

    def render(self, name, value, attrs=None, renderer=None):
        site_key = self.site_key or get_setting("SITE_KEY")
        ctype = self.type or get_setting("TYPE")
        theme = self.theme or get_setting("THEME")
        base = get_setting("BASE_URL").rstrip("/")
        field_name = get_setting("TOKEN_FIELD")

        if not site_key:
            return mark_safe(
                '<div style="color:#b00;font-size:13px;">'
                "LazyCaptcha site key is not configured (LAZYCAPTCHA['SITE_KEY'])."
                "</div>"
            )

        # The widget JS injects a hidden input named `lazycaptcha-token` into the
        # parent form automatically. We include a fallback hidden input to
        # preserve the submitted value during validation error re-renders.
        html = (
            f'<div class="lazycaptcha" data-sitekey="{site_key}" '
            f'data-type="{ctype}" data-theme="{theme}"></div>'
            f'<script src="{base}/api/captcha/v1/lazycaptcha.js" async defer></script>'
        )
        # Fallback hidden input (usually overwritten by widget JS)
        if name and name != field_name:
            html += f'<input type="hidden" name="{field_name}" value="{value or ""}">'

        return mark_safe(html)

    def value_from_datadict(self, data, files, name):
        # Ignore Django-generated field name; read the fixed widget field
        return data.get(get_setting("TOKEN_FIELD"), "")
