from typing import Optional
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator, MaxLengthValidator
from datetime import date
from . import messages
from django.db.models.manager import Manager


class Contact(models.Model):
    objects = models.Manager()
    full_name: models.CharField = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, messages.ERROR_NAME_TOO_SHORT),
            MaxLengthValidator(100, messages.ERROR_NAME_TOO_LONG)
        ]
    )
    address: models.CharField = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(5, messages.ERROR_ADDRESS_TOO_SHORT),
            MaxLengthValidator(200, messages.ERROR_ADDRESS_TOO_LONG)
        ]
    )
    email: models.EmailField = models.EmailField(
        validators=[EmailValidator(messages.INVALID_EMAIL)]
    )
    phone: models.CharField = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+38 \(\d{3}\) \d{3}-\d{2}-\d{2}$',
                message=messages.INVALID_PHONE_FORMAT
            )
        ]
    )
    birthday: models.DateField = models.DateField()
    user: Optional[User] = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='contacts'
    )

    def clean(self):
        if self.birthday is not None and self.birthday > date.today():
            raise ValidationError({'birthday': messages.BIRTHDAY_IN_FUTURE})

    def __str__(self) -> str:
        return self.full_name if self.full_name is not None else ''
