"""LazyCaptcha integration for Django."""

from lazycaptcha.client import LazyCaptchaClient, verify, check
from lazycaptcha.fields import LazyCaptchaField
from lazycaptcha.widgets import LazyCaptchaWidget
from lazycaptcha.forms import LazyCaptchaFormMixin

__all__ = [
    "LazyCaptchaClient",
    "LazyCaptchaField",
    "LazyCaptchaWidget",
    "LazyCaptchaFormMixin",
    "verify",
    "check",
]

__version__ = "2.0.0"

default_app_config = "lazycaptcha.apps.LazyCaptchaConfig"
