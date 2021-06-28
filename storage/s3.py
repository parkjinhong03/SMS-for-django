import boto3
from django.conf import settings
from _meta.singleton import Singleton


class S3Storage(metaclass=Singleton):
    """object storage using AWS S3"""

    def __init__(self, access_id: str = settings.AWS_S3_ID, access_key: str = settings.AWS_S3_KEY):
        self.client = boto3.client('s3', aws_access_key_id=access_id, aws_secret_access_key=access_key)

    def put_object(self, body, key, bucket=settings.AWS_S3_BUCKET, acl='public-read') -> None:
        self.client.put_object(ACL=acl, Body=body, Bucket=bucket, Key=key)
