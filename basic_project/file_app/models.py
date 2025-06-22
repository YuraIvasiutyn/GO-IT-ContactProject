from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    CATEGORY_CHOICES = [
        ('image', 'Зображення'),
        ('document', 'Документ'),
        ('video', 'Відео'),
        ('other', 'Інше'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    file_url = models.URLField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name if self.file else self.file_url} ({self.category})"
