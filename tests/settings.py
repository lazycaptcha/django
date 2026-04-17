SECRET_KEY = "test-secret-for-tests-only"
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
}
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "lazycaptcha",
]
USE_TZ = True

LAZYCAPTCHA = {
    "SITE_KEY": "test-site-key",
    "SECRET_KEY": "test-secret-key",
    "BASE_URL": "https://example.com",
}
