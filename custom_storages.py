import logging
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION

try:
    AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
    AWS_S3_REGION_NAME = settings.AWS_S3_REGION_NAME
    logger.info(f"AWS S3 storage configured for bucket '{AWS_STORAGE_BUCKET_NAME}'")
except AttributeError as e:
    logger.error(f"AWS settings are not properly configured: {e}")