"""
URL configuration for the ``note_app`` module.

This module contains all the URL routes for the Notes feature of the Personal Assistant app.
Each route maps a URL path to its corresponding view function.

Routes are grouped into:
- Notes operations (create/edit/delete/view)
- Tag operations (create/edit/delete/filter)

App name:
    ``note_app``

Example:
    Use with Django's reverse() function:
        >>> reverse("note_app:note-main")

Attributes:
    app_name (str): The application namespace.
    urlpatterns (list): List of URL route definitions.
"""

from django.urls import path
from . import views


app_name = 'note_app'

#: List of URL patterns for note and tag operations
urlpatterns = [
    #: URL pattern to access the main dashboard of notes
    path('main/', views.main, name='note-main'),

    #: URL pattern to create a new tag or list existing tags
    path('tag/', views.tag, name='note-tag'),

    #: URL pattern to view notes associated with a specific tag
    path('tag/<str:tag_name>', views.search_by_tag, name='notes-by-tag'),

    #: URL pattern to edit a tag by its ID
    path('tag/edit/<int:tag_id>/', views.edit_tag, name='notes-tag-edit'),

    #: URL pattern to delete a tag by its ID
    path('tag/delete/<int:tag_id>/', views.delete_tag, name='notes-tag-delete'),

    #: URL pattern to create a new note
    path('note/', views.note, name='note'),

    #: URL pattern to edit an existing note by ID
    path('note/edit/<int:note_id>/', views.note, name='note-edit'),

    #: URL pattern to update the color of a note
    path('note/color/<int:note_id>/', views.update_note_color, name='note-color-update'),

    #: URL pattern to delete a note
    path('note/delete/<int:note_id>/', views.note_delete, name='note-delete'),
]
