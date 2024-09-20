# urls.py (in the videos app)
from django.urls import path
from .views import VideoListView, VideoUploadView

urlpatterns = [
    path('', VideoListView.as_view(), name='video_list'),
    path('upload/', VideoUploadView.as_view(), name='video_upload'),
]