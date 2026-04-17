import json

import pytest
import responses

from lazycaptcha.client import LazyCaptchaClient


@pytest.fixture
def client():
    return LazyCaptchaClient()


def test_verify_returns_failure_for_empty_token(client):
    result = client.verify("")
    assert result["success"] is False
    assert result["error"] == "missing_token"


@responses.activate
def test_verify_calls_correct_endpoint(client):
    responses.post(
        "https://example.com/api/captcha/v1/verify",
        json={"success": True, "score": 0.87, "hostname": "example.org"},
        status=200,
    )
    result = client.verify("valid-token", "1.2.3.4")
    assert result["success"] is True
    assert result["score"] == 0.87

    sent = responses.calls[0].request
    body = json.loads(sent.body)
    assert body["secret"] == "test-secret-key"
    assert body["token"] == "valid-token"
    assert body["remote_ip"] == "1.2.3.4"


@responses.activate
def test_verify_handles_http_error(client):
    responses.post(
        "https://example.com/api/captcha/v1/verify",
        body=responses.ConnectionError("timeout"),
    )
    result = client.verify("token")
    assert result["success"] is False
    assert result["error"] == "request_failed"


@responses.activate
def test_check_returns_boolean(client):
    responses.post(
        "https://example.com/api/captcha/v1/verify",
        json={"success": True},
        status=200,
    )
    assert client.check("token") is True
