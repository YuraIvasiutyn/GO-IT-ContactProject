from typing import List
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name: str = 'contact_app'

urlpatterns: List[URLPattern] = [
    path('', views.main, name='main'),
    path('add_contact/', views.add_contact, name='add_contact'),
    path('edit_contact/<int:pk>', views.edit_contact, name='edit_contact'),
    path('delete_confirm/<int:pk>', views.delete_contact, name='delete_confirm'),
]