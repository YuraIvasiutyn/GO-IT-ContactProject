from django.db import models


# Create your models here.
class ExchangeRate(models.Model):
    currency_code = models.CharField(max_length=3)
    currency_name = models.CharField(max_length=50)
    rate = models.FloatField()
    date = models.DateField()

    class Meta:
        unique_together = ['currency_code', 'date']
