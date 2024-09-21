from django.db import models
from django.core.exceptions import ValidationError
import os
from storages.backends.s3boto3 import S3Boto3Storage

def validate_video_extension(value):
    valid_extensions = ['.mp4', '.avi', '.mov', '.flv', '.wmv', '.webm', '.mkv']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f'Unsupported file extension. Allowed extensions are: {", ".join(valid_extensions)}')

class S3MediaStorage(S3Boto3Storage):
    location = 'media'

class Video(models.Model):
    VIDEO_FORMATS = [
        ('mp4', 'MP4'),
        ('avi', 'AVI'),
        ('mov', 'MOV'),
        ('flv', 'FLV'),
        ('wmv', 'WMV'),
        ('webm', 'WebM'),
        ('mkv', 'MKV'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True, storage=S3MediaStorage())
    video_file = models.FileField(upload_to='videos/', validators=[validate_video_extension], storage=S3MediaStorage())
    video_format = models.CharField(max_length=4, choices=VIDEO_FORMATS, editable=False)
    view_count = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.video_file:
            ext = os.path.splitext(self.video_file.name)[1][1:].lower()
            format_dict = dict((k.lower(), k) for k, v in self.VIDEO_FORMATS)
            if ext in format_dict:
                self.video_format = format_dict[ext]
            else:
                raise ValidationError(f'Unsupported file extension. Allowed extensions are: {", ".join([f".{k}" for k in format_dict.keys()])}')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    video = models.ForeignKey(Video, related_name='comments', on_delete=models.CASCADE)
    user = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.video.title}'
