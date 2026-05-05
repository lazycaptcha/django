"""
LazyCaptcha settings resolution.

Settings live under the ``LAZYCAPTCHA`` dict in Django settings:

    LAZYCAPTCHA = {
        "SITE_KEY": "...",
        "SECRET_KEY": "...",
        "BASE_URL": "https://lazycaptcha.com",
        "TIMEOUT": 5,
        "TYPE": "auto",
        "THEME": "light",
        "WIDGET": "standard",
        "WIDTH": "",
        "TOKEN_FIELD": "lazycaptcha-token",
        "SEND_REMOTE_IP": True,
    }
"""

from __future__ import annotations

from django.conf import settings


DEFAULTS = {
    "SITE_KEY": "",
    "SECRET_KEY": "",
    "BASE_URL": "https://lazycaptcha.com",
    "TIMEOUT": 5,
    "TYPE": "auto",
    "THEME": "light",
    "WIDGET": "standard",
    "WIDTH": "",
    "TOKEN_FIELD": "lazycaptcha-token",
    "SEND_REMOTE_IP": True,
}


def get_setting(key: str):
    user_settings = getattr(settings, "LAZYCAPTCHA", {}) or {}
    if key in user_settings:
        return user_settings[key]
    return DEFAULTS[key]


def all_settings() -> dict:
    return {k: get_setting(k) for k in DEFAULTS}
