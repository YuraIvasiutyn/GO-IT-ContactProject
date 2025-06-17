from django.db import models

# Create your models here.


# Зберігати контакти з іменами, адресами, номерами телефонів, email та днями народження до книги контактів;
# Виводити список контактів, у яких день народження через задану кількість днів від поточної дати;
# Перевіряти правильність введеного номера телефону та email під час створення або редагування запису та повідомляти користувача у разі некоректного введення;
# Здійснювати пошук контактів серед контактів книги;
# Редагувати та видаляти записи з книги контактів;


class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    birthday = models.DateField()

    def __str__(self):
        return self.full_name