from django.contrib import admin
from django.urls import path, include
from . import views




app_name = 'file_app'

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
]
