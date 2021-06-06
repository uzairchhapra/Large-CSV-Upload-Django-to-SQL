from django.db import models
from chunked_upload.models import AbstractChunkedUpload
from django.conf import settings

# Create your models here.

# 'ChunkedUpload' class provides almost everything for you.
# if you need to tweak it little further, create a model class
# by inheriting "chunked_upload.models.AbstractChunkedUpload" class


class MyChunkedUpload(AbstractChunkedUpload):
    def delete(self, delete_file=False, *args, **kwargs):
        if self.file:
            storage, path = self.file.storage, self.file.path
        super(AbstractChunkedUpload, self).delete(*args, **kwargs)
        if self.file and delete_file:
            storage.delete(path)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chunk_upload',
        null=settings.DEFAULT_MODEL_USER_FIELD_NULL,
        blank=settings.DEFAULT_MODEL_USER_FIELD_BLANK
    )

    # MyChunkedUpload = ChunkedUpload
