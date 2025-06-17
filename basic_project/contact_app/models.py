from django.db import models

# Create your models here.



class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    birthday = models.DateField()

    def __str__(self):
        return self.full_name