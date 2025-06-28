from django.forms import Form, ModelForm, NumberInput, IntegerField, CharField, EmailField, DateField, TextInput, \
    EmailInput, DateInput
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date
from .models import Contact
from . import messages


class QueryForm(Form):
    query = CharField(
        max_length=100, required=False, label='Search',
        widget=TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Search', 'id': 'query'
        })
    )
    days = IntegerField(
        required=False, min_value=0, max_value=365, label='Days to birthday',
        widget=NumberInput(attrs={
            'class': 'form-control', 'placeholder': '365', 'type': 'number', 'id': 'days'
        })
    )


class AddContactForm(ModelForm):
    full_name = CharField(
        max_length=100, min_length=2, required=True, label='Full name', help_text='Enter full name',
        error_messages={
            'required': messages.ERROR_FIELD_REQUIRED,
            'min_length': messages.ERROR_NAME_TOO_SHORT,
            'max_length': messages.ERROR_NAME_TOO_LONG if hasattr(messages,
                                                                  'ERROR_NAME_TOO_LONG') else 'Name is too long',
        },
        widget=TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Enter full name', 'id': 'full_name'
        })
    )
    address = CharField(
        max_length=200, min_length=5, required=True, label='Address', help_text='Enter address',
        error_messages={
            'required': messages.ERROR_FIELD_REQUIRED,
            'min_length': messages.ERROR_ADDRESS_TOO_SHORT if hasattr(messages,
                                                                      'ERROR_ADDRESS_TOO_SHORT') else 'Address is too short',
            'max_length': messages.ERROR_ADDRESS_TOO_LONG if hasattr(messages,
                                                                     'ERROR_ADDRESS_TOO_LONG') else 'Address is too long',
        },
        widget=TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Enter address', 'id': 'address'
        })
    )
    email = EmailField(
        required=True, label='Email', help_text='Enter email',
        error_messages={
            'required': messages.ERROR_FIELD_REQUIRED,
            'invalid': messages.INVALID_EMAIL if hasattr(messages, 'INVALID_EMAIL') else 'Enter a valid email address',
        },
        widget=EmailInput(attrs={
            'class': 'form-control', 'placeholder': 'Enter email', 'id': 'email'
        })
    )
    phone = CharField(
        max_length=20, required=True, label='Phone', help_text='Enter phone',
        validators=[RegexValidator(
            regex=r'^\+38 \(\d{3}\) \d{3}-\d{2}-\d{2}$',
            message=messages.INVALID_PHONE_FORMAT if hasattr(messages,
                                                             'INVALID_PHONE_FORMAT') else "Phone number must be entered in the format: '+38 (XXX) XXX-XX-XX'."
        )],
        error_messages={
            'required': messages.ERROR_FIELD_REQUIRED,
            'invalid': messages.INVALID_PHONE_FORMAT if hasattr(messages,
                                                                'INVALID_PHONE_FORMAT') else "Invalid phone format",
        },
        widget=TextInput(attrs={
            'class': 'form-control', 'placeholder': '+38 (xxx) xxx-xx-xx', 'id': 'phone'
        })
    )
    birthday = DateField(
        required=True, label='Birthday', help_text='Enter birthday',
        error_messages={
            'required': messages.ERROR_FIELD_REQUIRED,
            'invalid': messages.ERROR_BIRTHDAY_INVALID if hasattr(messages,
                                                                  'ERROR_BIRTHDAY_INVALID') else "Enter a valid date",
        },
        widget=DateInput(attrs={
            'class': 'form-control', 'type': 'date', 'placeholder': 'Enter birthday', 'id': 'birthday'
        })
    )

    class Meta:
        model = Contact
        fields = ['full_name', 'address', 'email', 'phone', 'birthday']

    def clean_birthday(self):
        """
        Validate the birthday field to ensure it is not set to a future date.

        Raises:
            ValidationError: If the birthday is set to a future date.

        Returns:
            The validated birthday date.
        """

        birthday = self.cleaned_data.get('birthday')
        if birthday and birthday > date.today():
            raise ValidationError(messages.ERROR_BIRTHDAY_IN_FUTURE if hasattr(messages,
                                                                               'ERROR_BIRTHDAY_IN_FUTURE') else "Birthday cannot be in the future")
        return birthday
