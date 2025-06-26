from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """
    Model representing a user-defined tag for notes.

    Attributes:
        name (str): Name of the tag (must be unique per user).
        user (User): Reference to the user who owns the tag.

    Meta:
        constraints: Ensures that each tag name is unique per user.

    Methods:
        __str__(): Returns a human-readable string representation of the tag.
    """
    name = models.CharField(max_length=50, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'user'],
                name='unique_tag_for_user')
        ]

    def __str__(self):
        """
        Return the tag's name as its string representation.
        """
        return f"{self.name}"


class Note(models.Model):
    """
    Model representing a personal note belonging to a user.

    Attributes:
        note_title (str): Title of the note.
        note (str): Content of the note (optional).
        created (datetime): Timestamp when the note was created.
        last_modified_at (datetime): Timestamp of the last modification.
        tags (ManyToMany[Tag]): Tags associated with this note.
        user (User): Reference to the user who owns the note.
        color (str): Background color of the note in HEX format.

    Meta:
        constraints: Ensures that each note title is unique per user.

    Methods:
        __str__(): Returns the note title as its string representation.
    """
    note_title = models.CharField(max_length=500, null=False, blank=False)
    note = models.CharField(
        max_length=5000,
        null=True,
        unique=False,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=-1)
    color = models.CharField(max_length=20, default="#ffffff")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['note_title', 'user'],
                name='unique_note_for_user')
        ]

    def __str__(self):
        """
        Return the note's title as its string representation.
        """
        return f"{self.note_title}"
