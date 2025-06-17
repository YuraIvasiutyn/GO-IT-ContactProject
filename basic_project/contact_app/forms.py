from django.forms import ModelForm, CharField, EmailField, DateField, TextInput, EmailInput, DateInput
from django import forms
from .models import Contact


class QueryForm(forms.Form):
    q = forms.CharField(
        max_length=100,
        label='Search',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search',
            'id': 'q'
        })
    )


class AddContactForm(ModelForm):
    full_name = CharField(
        max_length=100, min_length=4, required=True, label='Full name', help_text='Enter full name',
        error_messages={
            'required': 'This field is required',
            'min_length': 'This field is too short'
        },
        widget=TextInput(attrs={
            'class': 'form-control', 'type': 'text', 'placeholder': 'Enter full name', 'id': 'full_name'
        })
    )
    address = CharField(
        max_length=200, required=True, label='Address', help_text='Enter address',
        widget=TextInput(attrs={
            'class': 'form-control', 'type': 'text', 'placeholder': 'Enter address', 'id': 'address'
        })
    )
    email = EmailField(
        required=True, label='Email', help_text='Enter email',
        widget=EmailInput(attrs={
            'class': 'form-control', 'type': 'email', 'placeholder': 'Enter email', 'id': 'email'
        })
    )
    phone = CharField(
        max_length=20, required=True, label='Phone', help_text='Enter phone',
        widget=TextInput(attrs={
            'class': 'form-control', 'type': 'tel', 'placeholder': '+38 (xxx) xxx-xx-xx', 'id': 'phone'
        })
    )
    birthday = DateField(
        required=True, label='Birthday', help_text='Enter birthday',
        widget=DateInput(attrs={
            'class': 'form-control', 'type': 'date', 'placeholder': 'Enter birthday', 'id': 'birthday'
        })
    )

    class Meta:
        model = Contact
        fields = ['full_name', 'address', 'email', 'phone', 'birthday']
