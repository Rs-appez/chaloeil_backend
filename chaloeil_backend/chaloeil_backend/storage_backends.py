from uuid import uuid4
from storages.backends.s3boto3 import S3Boto3Storage


def rename_file(instance, filename):
    """
    Rename file name with UUID
    """
    ext = filename.split(".")[-1]
    new_filename = f"{uuid4()}.{ext}"
    return new_filename


class QuestionMediaStorage(S3Boto3Storage):
    location = "question_media"
    file_overwrite = False
