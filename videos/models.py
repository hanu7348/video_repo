# Step 3: Update models.py
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    file = models.FileField(storage=S3Boto3Storage())
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
