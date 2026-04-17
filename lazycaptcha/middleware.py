"""
Middleware that enforces captcha verification on configured URL prefixes.

Add to MIDDLEWARE and set LAZYCAPTCHA['PROTECTED_PATHS'] in settings:

    LAZYCAPTCHA = {
        ...,
        'PROTECTED_PATHS': ['/contact/', '/signup/'],
    }
"""

from __future__ import annotations

from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse

from lazycaptcha.client import LazyCaptchaClient
from lazycaptcha.conf import get_setting
from lazycaptcha.forms import _client_ip


class LazyCaptchaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_paths: list[str] = list(
            getattr(settings, "LAZYCAPTCHA", {}).get("PROTECTED_PATHS", [])
        )
        self.client = LazyCaptchaClient()

    def __call__(self, request):
        if request.method == "POST" and self._is_protected(request.path):
            token = request.POST.get(get_setting("TOKEN_FIELD"), "")
            if not self.client.check(token, _client_ip(request)):
                if request.headers.get("Accept", "").startswith("application/json"):
                    return JsonResponse({"error": "captcha_failed"}, status=422)
                return HttpResponseBadRequest("Captcha verification failed.")
        return self.get_response(request)

    def _is_protected(self, path: str) -> bool:
        return any(path.startswith(p) for p in self.protected_paths)
