from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    CATEGORY_CHOICES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = models.CharField(max_length=500)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} ({self.category})"
