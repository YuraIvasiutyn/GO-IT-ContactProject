from django.urls import path

from . import views

app_name = 'contact_app'

urlpatterns = [
    path('', views.main, name='main'),
    path('add_contact/', views.add_contact, name='add_contact'),
    path('edit_contact/<int:pk>', views.edit_contact, name='edit_contact'),
    path('delete_confirm/<int:pk>', views.delete_contact, name='delete_confirm'),
]
