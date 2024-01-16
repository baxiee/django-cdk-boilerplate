# flake8: noqa
import os

from settings.base import *


SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = False

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["RDS_DBNAME"],
        "USER": os.environ["RDS_USERNAME"],
        "HOST": os.environ["RDS_HOST"],
        "PASSWORD": os.environ["RDS_PASSWORD"],
        "PORT": os.environ["RDS_PORT"],
        "OPTIONS": {"connect_timeout": 60},
    }
}

REST_FRAMEWORK.update(
    {"DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",)}
)

STATIC_URL = "/static/"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_STORAGE_BUCKET_NAME = os.getenv("STATIC_BUCKET_NAME")
AWS_MEDIA_STORAGE_BUCKET_NAME = os.getenv("STATIC_BUCKET_NAME")
# AWS_QUERYSTRING_AUTH = False #TODO check in some day if it works with false (waiting for AWS to process everything)
AWS_DEFAULT_ACL = None
