"""HTTP client for the LazyCaptcha verification API."""

from __future__ import annotations

import logging
from typing import Any

import requests

from lazycaptcha.conf import get_setting

logger = logging.getLogger("lazycaptcha")


class LazyCaptchaClient:
    def __init__(
        self,
        secret_key: str | None = None,
        base_url: str | None = None,
        timeout: int | None = None,
        send_remote_ip: bool | None = None,
    ):
        self.secret_key = secret_key if secret_key is not None else get_setting("SECRET_KEY")
        self.base_url = (base_url if base_url is not None else get_setting("BASE_URL")).rstrip("/")
        self.timeout = timeout if timeout is not None else get_setting("TIMEOUT")
        self.send_remote_ip = send_remote_ip if send_remote_ip is not None else get_setting("SEND_REMOTE_IP")

    def verify(self, token: str, remote_ip: str | None = None) -> dict[str, Any]:
        if not token:
            return {"success": False, "error": "missing_token"}
        if not self.secret_key:
            return {"success": False, "error": "missing_secret_config"}

        payload: dict[str, Any] = {"secret": self.secret_key, "token": token}
        if remote_ip and self.send_remote_ip:
            payload["remote_ip"] = remote_ip

        try:
            resp = requests.post(
                f"{self.base_url}/api/captcha/v1/verify",
                json=payload,
                headers={"Accept": "application/json"},
                timeout=self.timeout,
            )
        except requests.RequestException as e:
            logger.warning("LazyCaptcha verify request failed: %s", e)
            return {"success": False, "error": "request_failed", "detail": str(e)}

        try:
            body = resp.json()
        except ValueError:
            return {"success": False, "error": "invalid_response"}

        if not isinstance(body, dict):
            return {"success": False, "error": "invalid_response"}

        return body

    def check(self, token: str, remote_ip: str | None = None) -> bool:
        return bool(self.verify(token, remote_ip).get("success"))


# Convenience module-level helpers
_default_client: LazyCaptchaClient | None = None


def _client() -> LazyCaptchaClient:
    global _default_client
    if _default_client is None:
        _default_client = LazyCaptchaClient()
    return _default_client


def verify(token: str, remote_ip: str | None = None) -> dict[str, Any]:
    return _client().verify(token, remote_ip)


def check(token: str, remote_ip: str | None = None) -> bool:
    return _client().check(token, remote_ip)
