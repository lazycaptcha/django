"""Template tag: {% load lazycaptcha %}{% lazycaptcha %}"""

from __future__ import annotations

from django import template
from django.utils.safestring import mark_safe

from lazycaptcha.conf import get_setting

register = template.Library()


@register.simple_tag
def lazycaptcha(type: str | None = None, theme: str | None = None, site_key: str | None = None):
    site_key = site_key or get_setting("SITE_KEY")
    ctype = type or get_setting("TYPE")
    theme = theme or get_setting("THEME")
    base = get_setting("BASE_URL").rstrip("/")

    if not site_key:
        return mark_safe(
            '<div style="color:#b00;font-size:13px;">'
            "LazyCaptcha site key is not configured."
            "</div>"
        )

    return mark_safe(
        f'<div class="lazycaptcha" data-sitekey="{site_key}" '
        f'data-type="{ctype}" data-theme="{theme}"></div>'
        f'<script src="{base}/api/captcha/v1/lazycaptcha.js" async defer></script>'
    )


@register.simple_tag
def lazycaptcha_script():
    """Outputs just the script tag if you want to place it separately."""
    base = get_setting("BASE_URL").rstrip("/")
    return mark_safe(
        f'<script src="{base}/api/captcha/v1/lazycaptcha.js" async defer></script>'
    )
