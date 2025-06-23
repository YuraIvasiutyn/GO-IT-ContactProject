from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import File
from .forms import FileUploadForm


@login_required
def upload_file(request):
    if request.method == 'POST':
        file_url = request.POST.get('file')
        category = request.POST.get('category')
        if file_url and category:
            File.objects.create(user=request.user, file=file_url, category=category)
            return redirect('file_app:file_list')
    return render(request, 'file_app/upload.html', {
        'uploadcare_public_key': settings.UPLOADCARE_PUBLIC_KEY
    })


@login_required
def file_list(request):
    category = request.GET.get('category')
    files = File.objects.filter(user=request.user)
    if category:
        files = files.filter(category=category)
    return render(request, 'file_app/file_list.html', {'files': files})
