from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=4, name='name')
    amount = models.IntegerField(name='amount')
    buy_price = models.FloatField(name='buy_price')
    time_buy = models.DateTimeField(name='time_buy')
    description = models.TextField(max_length=100, name='description')