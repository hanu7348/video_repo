from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_list, name='video_list'),
    path('upload/', views.upload_video, name='upload_video'),
    path('video/<int:pk>/', views.video_detail, name='video_detail'),
    path('video/<int:pk>/like/', views.update_likes_dislikes, {'action': 'like'}, name='like_video'),
    path('video/<int:pk>/dislike/', views.update_likes_dislikes, {'action': 'dislike'}, name='dislike_video'),
]
