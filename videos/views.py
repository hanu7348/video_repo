from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from .models import Video, Comment
from .forms import VideoForm, CommentForm
from storages.backends.s3boto3 import S3Boto3Storage

s3_storage = S3Boto3Storage()

def get_s3_url(file_name):
    return s3_storage.url(file_name)

def video_list(request):
    videos = Video.objects.all().order_by('-uploaded_at')
    for video in videos:
        if video.thumbnail:
            video.thumbnail_url = get_s3_url(video.thumbnail.name)
        video.video_url = get_s3_url(video.video_file.name)
    return render(request, 'video_list.html', {'videos': videos})

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            return redirect('video_detail', pk=video.pk)
    else:
        form = VideoForm()
    return render(request, 'video_upload.html', {'form': form})

def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video.view_count += 1
    video.save()

    video.video_url = get_s3_url(video.video_file.name)
    if video.thumbnail:
        video.thumbnail_url = get_s3_url(video.thumbnail.name)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.video = video
            comment.save()
            return redirect('video_detail', pk=pk)
    else:
        comment_form = CommentForm()

    comments = video.comments.all().order_by('-timestamp')

    other_videos = Video.objects.exclude(pk=pk).order_by('-uploaded_at')[:6]
    for other_video in other_videos:
        if other_video.thumbnail:
            other_video.thumbnail_url = get_s3_url(other_video.thumbnail.name)
        other_video.video_url = get_s3_url(other_video.video_file.name)

    return render(request, 'video_detail.html', {
        'video': video,
        'comments': comments,
        'comment_form': comment_form,
        'other_videos': other_videos,
    })

def update_likes_dislikes(request, pk, action):
    video = get_object_or_404(Video, pk=pk)
    if action == 'like':
        video.likes += 1
    elif action == 'dislike':
        video.dislikes += 1
    video.save()
    return JsonResponse({'likes': video.likes, 'dislikes': video.dislikes})
