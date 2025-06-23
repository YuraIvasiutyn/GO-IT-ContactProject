from django.contrib import admin
from .models import File

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file', 'category', 'uploaded_at')
    list_filter = ('category', 'uploaded_at')
    search_fields = ('user__username', 'file')