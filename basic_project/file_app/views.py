from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import File
from .forms import FileUploadForm


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = form.save(commit=False)
            file_obj.user = request.user
            file_obj.save()
            return redirect('file_app:file_list')
    else:
        form = FileUploadForm()
    return render(request, 'file_app/upload.html', {'form': form})


@login_required
def file_list(request):
    category = request.GET.get('category')
    files = File.objects.filter(user=request.user)
    if category:
        files = files.filter(category=category)
    return render(request, 'file_app/file_list.html', {'files': files})
