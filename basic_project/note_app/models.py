from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'user'],
                name='unique_tag_for_user')
        ]

    def __str__(self):
        return f"{self.name}"


class Note(models.Model):
    note_title = models.CharField(max_length=500, null=False, blank=False)
    note = models.CharField(max_length=5000, null=True, unique=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=-1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['note_title', 'user'],
                name='unique_note_for_user')
        ]

    def __str__(self):
        return f"{self.note_title}"
