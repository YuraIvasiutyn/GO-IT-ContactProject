from django.urls import path
from . import views

app_name = 'note_app'

urlpatterns = [
    path('main/', views.main, name='note-main'),
    path('tag/', views.tag, name='note-tag'),
    path('tag/<str:tag_name>', views.search_by_tag, name='notes-by-tag'),

    path('note/', views.note, name='note'),
    path('note/edit/<int:note_id>/', views.note, name='note-edit'),
    path('note/delete/<int:note_id>/', views.note_delete, name='note-delete'),
    # path('note/search/<str:search_text>/', views.notes_search, name='note-search'),
]

