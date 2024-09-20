from django.shortcuts import render, redirect, get_object_or_404
from .models import Video, Comment
from .forms import VideoForm, CommentForm
from django.http import JsonResponse

def video_list(request):
    videos = Video.objects.all().order_by('-uploaded_at')
    return render(request, 'video_list.html', {'videos': videos})

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('video_list')
    else:
        form = VideoForm()
    return render(request, 'upload_video.html', {'form': form})

def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video.view_count += 1
    video.save()

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

    # Fetch other videos except the current one
    other_videos = Video.objects.exclude(pk=pk).order_by('-uploaded_at')[:6]

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

