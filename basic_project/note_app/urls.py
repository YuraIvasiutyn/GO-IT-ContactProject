from django.urls import path
from . import views

app_name = 'note_app'

urlpatterns = [
    path('', views.main, name='main'),
    path('error/<str:message>', views.error, name='error-page'),
    path('dev-login/', views.dev_login, name='dev-login'),


    path('tag/', views.tag, name='tag'),
    path('tag/<str:tag_name>', views.search_by_tag, name='notes-by-tag'),

    path('note/', views.note, name='note'),
    path('note/edit/<int:note_id>/', views.note, name='note-edit'),
    path('note/delete/<int:note_id>/', views.note_delete, name='note-delete'),
    # path('note/search/<str:search_text>/', views.notes_search, name='note-search'),
]
