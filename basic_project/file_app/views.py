from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .firebase_utils import upload_file_to_firebase
from .models import File

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            public_url = upload_file_to_firebase(uploaded_file)
            File.objects.create(
                user=request.user,
                file_url=public_url,
                category=form.cleaned_data['category']
            )
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'file_app/upload.html', {'form': form})

def file_list(request):
    files = File.objects.filter(user=request.user)
    return render(request, 'file_app/file_list.html', {'files': files})
