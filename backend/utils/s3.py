import os
from aiobotocore.session import get_session

AWS_ACCESS_KEY_ID = os.getenv("IMAGE_UPLOAD_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("IMAGE_UPLOAD_AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("IMAGE_UPLOAD_BUCKET_NAME")

# Create a global session and client instance
session = get_session()


async def initialize_s3_client():
    return session.create_client(
        "s3",
        region_name="us-east-1",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


async def upload_to_s3(file_data, object_name):
    s3_client = await initialize_s3_client()
    async with s3_client as client:
        await client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=object_name,
            Body=file_data,
            ContentType="image/jpeg",
        )


async def delete_from_s3(object_name):
    s3_client = await initialize_s3_client()
    async with s3_client as client:
        await client.delete_object(
            Bucket=S3_BUCKET_NAME,
            Key=object_name,
        )


async def create_presigned_url(object_name, expiration=604800):
    s3_client = await initialize_s3_client()
    async with s3_client as client:
        url = await client.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET_NAME, "Key": object_name},
            ExpiresIn=expiration,
        )
    return url
