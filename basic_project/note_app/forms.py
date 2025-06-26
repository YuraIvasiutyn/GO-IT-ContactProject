from django.forms import ModelForm, CharField, TextInput, Textarea
#  , DateField, DateInput, HiddenInput, IntegerField
from .models import Tag, Note
# from django import forms


class TagForm(ModelForm):
    """
    Form for creating or updating a tag.

    Fields:
        - name (CharField): The name of the tag. Required. Max length 50.
    """
    name = CharField(
        min_length=1,
        max_length=50,
        required=True,
        widget=TextInput()
    )

    class Meta:
        model = Tag
        fields = ['name']


class NoteForm(ModelForm):
    """
    Form for creating or editing a note.

    Fields:
        - note_title (CharField): The title of the note. Required. Max length 500.
        - note (CharField): The content of the note. Optional. Max length 5000.
    """
    note_title = CharField(
        min_length=1,
        max_length=500,
        required=True,
        widget=TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'put title of your note'
        })
    )
    note = CharField(
        max_length=5000,
        required=False,
        widget=Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'style': 'resize: vertical;',
            'placeholder': 'write your note here...'
        })
    )

    class Meta:
        model = Note
        fields = ['note_title', 'note']
        exclude = ['tags', 'created', 'last_modified_at']
