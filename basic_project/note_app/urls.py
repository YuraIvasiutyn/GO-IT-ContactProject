from django.urls import path
from . import views


app_name = 'note_app'

urlpatterns = [
    path('main/', views.main, name='note-main'),
    path('tag/', views.tag, name='note-tag'),
    path('tag/<str:tag_name>', views.search_by_tag, name='notes-by-tag'),
    path('tag/edit/<int:tag_id>/', views.edit_tag, name='notes-tag-edit'),
    path('tag/delete/<int:tag_id>/', views.delete_tag, name='notes-tag-delete'),

    path('note/', views.note, name='note'),
    path('note/edit/<int:note_id>/', views.note, name='note-edit'),
    path('note/color/<int:note_id>/', views.update_note_color, name='note-color-update'),
    path('note/delete/<int:note_id>/', views.note_delete, name='note-delete'),
]
