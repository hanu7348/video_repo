from django.shortcuts import render, redirect
from django.views import View
from .models import Video
from .forms import VideoUploadForm

class VideoListView(View):
    def get(self, request):
        videos = Video.objects.all().order_by('-uploaded_at')
        for video in videos:
            video.s3_url = video.file.url  # This will now be the S3 URL
        return render(request, 'video_list.html', {'videos': videos})

class VideoUploadView(View):
    def get(self, request):
        form = VideoUploadForm()
        return render(request, 'video_upload.html', {'form': form})

    def post(self, request):
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('video_list')
        return render(request, 'video_upload.html', {'form': form})
