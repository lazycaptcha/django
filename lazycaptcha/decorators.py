"""View decorators for token verification."""

from __future__ import annotations

from functools import wraps

from django.http import HttpResponseBadRequest, JsonResponse

from lazycaptcha.client import LazyCaptchaClient
from lazycaptcha.conf import get_setting
from lazycaptcha.forms import _client_ip


def require_lazycaptcha(view_func=None, *, methods=("POST",)):
    """
    Decorator: verifies the `lazycaptcha-token` from the request before calling
    the view. Rejects with 422 on failure.

    Usage::

        @require_lazycaptcha
        def contact_view(request):
            ...
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(request, *args, **kwargs):
            if request.method in methods:
                token_field = get_setting("TOKEN_FIELD")
                token = request.POST.get(token_field) or (
                    request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
                    if request.content_type == "application/json" else ""
                )
                client = LazyCaptchaClient()
                if not client.check(token or "", _client_ip(request)):
                    if "application/json" in (request.content_type or ""):
                        return JsonResponse(
                            {"error": "captcha_failed"}, status=422
                        )
                    return HttpResponseBadRequest(
                        "Captcha verification failed. Please go back and try again."
                    )
            return fn(request, *args, **kwargs)

        return wrapper

    if view_func is not None:
        return decorator(view_func)
    return decorator
