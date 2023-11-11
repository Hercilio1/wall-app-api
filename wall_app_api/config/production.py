import os
from .common import Common


class Production(Common):
    INSTALLED_APPS = Common.INSTALLED_APPS
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    # Site
    # https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ["*"]
    INSTALLED_APPS += ("gunicorn", )

    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    EMAIL_PORT = os.getenv('EMAIL_PORT', "")
    EMAIL_HOST = os.getenv('EMAIL_HOST', "")
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', "")
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', "")
