from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
