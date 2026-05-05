"""Template tag: {% load lazycaptcha %}{% lazycaptcha %}"""

from __future__ import annotations

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from lazycaptcha.conf import get_setting

register = template.Library()


@register.simple_tag
def lazycaptcha(
    type: str | None = None,
    theme: str | None = None,
    site_key: str | None = None,
    widget: str | None = None,
    width: str | None = None,
):
    site_key = site_key or get_setting("SITE_KEY")
    ctype = type or get_setting("TYPE")
    theme = theme or get_setting("THEME")
    widget = widget or get_setting("WIDGET")
    width = width or get_setting("WIDTH")
    base = get_setting("BASE_URL").rstrip("/")

    if not site_key:
        return mark_safe(
            '<div style="color:#b00;font-size:13px;">'
            "LazyCaptcha site key is not configured."
            "</div>"
        )

    width_attr = f' data-width="{escape(width)}"' if width else ""
    return mark_safe(
        f'<div class="lazycaptcha" data-sitekey="{escape(site_key)}" '
        f'data-type="{escape(ctype)}" data-theme="{escape(theme)}" '
        f'data-widget="{escape(widget)}"{width_attr}></div>'
        f'<script src="{escape(base)}/api/captcha/v1/lazycaptcha.js" async defer></script>'
    )


@register.simple_tag
def lazycaptcha_script():
    """Outputs just the script tag if you want to place it separately."""
    base = get_setting("BASE_URL").rstrip("/")
    return mark_safe(
        f'<script src="{escape(base)}/api/captcha/v1/lazycaptcha.js" async defer></script>'
    )
