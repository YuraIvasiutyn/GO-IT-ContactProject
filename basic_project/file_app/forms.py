from django import forms
from .models import File
from django.conf import settings


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file', 'category']
        widgets = {
            'file': forms.TextInput(attrs={
                'role': 'uploadcare-uploader',
                'data-public-key': settings.UPLOADCARE_PUBLIC_KEY,
            }),
        }
