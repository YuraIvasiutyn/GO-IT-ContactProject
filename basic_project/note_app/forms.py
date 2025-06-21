from django.forms import ModelForm, CharField, TextInput, Textarea
#, DateField, DateInput, HiddenInput, IntegerField
from .models import Tag, Note
from django import forms

class TagForm(ModelForm):
    name = CharField(min_length=1, max_length=50, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class NoteForm(ModelForm):
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
