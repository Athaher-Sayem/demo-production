import os
from .settings import *
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = [
item.strip()
for item in os.environ["DJANGO_ALLOWED_HOSTS"].split(",")
if item.strip()
]
CSRF_TRUSTED_ORIGINS = [
item.strip()
for item in os.environ.get(
"DJANGO_CSRF_TRUSTED_ORIGINS", ""
).split(",")
if item.strip()
]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = os.environ.get("DJANGO_HTTPS", "0") == "1"
SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT
CSRF_COOKIE_SECURE = SECURE_SSL_REDIRECT
SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False


DATABASES = {
"default": {
"ENGINE": "django.db.backends.postgresql",
"NAME": os.environ["POSTGRES_DB"],
"USER": os.environ["POSTGRES_USER"],
"PASSWORD": os.environ["POSTGRES_PASSWORD"],
"HOST": "127.0.0.1",
"PORT": "5432",
}
}
STATIC_URL = "/static/"
STATIC_ROOT = "/var/www/demo-production/static"
FILE_UPLOAD_PERMISSIONS = 0o640
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o750
LOGGING = {
"version": 1,
"disable_existing_loggers": False,
"handlers": {"console": {"class": "logging.StreamHandler"}},
"root": {"handlers": ["console"], "level": "INFO"},
"loggers": {
"django": {
"handlers": ["console"],
"level": "INFO",
"propagate": False,
}
},
}
