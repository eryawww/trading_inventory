from django.db import models
import pytz

TIME_ZONE = pytz.timezone('Asia/Singapore')
# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=4, name='name')
    amount = models.FloatField(name='amount')
    buy_price = models.FloatField(name='buy_price')
    time_buy = models.DateTimeField(name='time_buy')
    description = models.TextField(max_length=100, name='description')