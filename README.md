# LazyCaptcha for Django

Drop-in Django integration for [LazyCaptcha](https://lazycaptcha.com). Adds a form field, widget, template tag, view decorator, and middleware.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/lazycaptcha-django.svg)](https://pypi.org/project/lazycaptcha-django/)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2%20%7C%205.x-green.svg)](https://www.djangoproject.com/)

## Installation

```bash
pip install lazycaptcha-django
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "lazycaptcha",
]
```

Configure keys in `settings.py`:

```python
LAZYCAPTCHA = {
    "SITE_KEY": "your-site-key-uuid",
    "SECRET_KEY": "your-secret-hex",
    "BASE_URL": "https://lazycaptcha.com",  # or your self-hosted instance
    # Optional:
    "TIMEOUT": 5,
    "TYPE": "auto",        # auto | image_puzzle | pow | behavioral | text_math
    "THEME": "light",      # light | dark
}
```

## Usage

### 1. Form field (recommended)

```python
from django import forms
from lazycaptcha import LazyCaptchaField, LazyCaptchaFormMixin


class ContactForm(LazyCaptchaFormMixin, forms.Form):
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    captcha = LazyCaptchaField()
```

```python
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST, request=request)
        if form.is_valid():
            # ... save/send
            return redirect("thanks")
    else:
        form = ContactForm(request=request)
    return render(request, "contact.html", {"form": form})
```

```django
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Send</button>
</form>
```

Optional: require a minimum risk score:

```python
captcha = LazyCaptchaField(min_score=0.5)
```

### 2. Template tag

If you don't want a form field (e.g. you're handling the form manually), use the template tag:

```django
{% load lazycaptcha %}
<form method="post">
    {% csrf_token %}
    <input name="email" type="email" required>
    {% lazycaptcha %}
    <button type="submit">Submit</button>
</form>
```

Override type/theme per-render:

```django
{% lazycaptcha type="image_puzzle" theme="dark" %}
```

### 3. View decorator

```python
from lazycaptcha.decorators import require_lazycaptcha

@require_lazycaptcha
def contact_view(request):
    # Token already verified; request.POST has the rest of the form
    ...
```

### 4. Middleware (verify on specific URL prefixes)

```python
MIDDLEWARE = [
    ...
    "lazycaptcha.middleware.LazyCaptchaMiddleware",
]

LAZYCAPTCHA = {
    ...,
    "PROTECTED_PATHS": ["/contact/", "/signup/"],
}
```

### 5. Low-level client

```python
from lazycaptcha import verify, check

result = verify(request.POST.get("lazycaptcha-token"), request.META.get("REMOTE_ADDR"))
if result["success"]:
    ...

# Or just a boolean
if check(token, remote_ip):
    ...
```

## Testing

When writing tests for views that use LazyCaptcha, mock `LazyCaptchaClient.check` with `responses`:

```python
import responses

@responses.activate
def test_contact_form_with_valid_captcha():
    responses.post(
        "https://lazycaptcha.com/api/captcha/v1/verify",
        json={"success": True, "score": 1.0},
    )

    response = client.post("/contact/", {
        "email": "a@b.c",
        "message": "hi",
        "lazycaptcha-token": "anything",
    })
    assert response.status_code == 302
```

Or patch directly:

```python
from unittest.mock import patch

with patch("lazycaptcha.client.LazyCaptchaClient.check", return_value=True):
    ...
```

## Configuration reference

| Key | Default | Purpose |
|-----|---------|---------|
| `SITE_KEY` | — | Public site key |
| `SECRET_KEY` | — | Private secret key |
| `BASE_URL` | `https://lazycaptcha.com` | LazyCaptcha instance |
| `TIMEOUT` | `5` | HTTP timeout in seconds |
| `TYPE` | `auto` | Default challenge type |
| `THEME` | `light` | Widget theme |
| `TOKEN_FIELD` | `lazycaptcha-token` | Form field name |
| `SEND_REMOTE_IP` | `True` | Forward client IP on verify |
| `PROTECTED_PATHS` | `[]` | Middleware URL prefixes |

## Compatibility

- Python 3.9, 3.10, 3.11, 3.12, 3.13
- Django 4.2, 5.0, 5.1

## License

[MIT](LICENSE)
