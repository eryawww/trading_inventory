from django.db import models
from django.contrib.auth.models import User
import pytz

TIME_ZONE = pytz.timezone('Asia/Singapore')
# Create your models here.
class Item(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=4, name='name')
    amount = models.IntegerField(name='amount')
    buy_price = models.FloatField(name='buy_price')
    time_buy = models.DateTimeField(name='time_buy', auto_now_add=True)
    description = models.TextField(max_length=30, name='description')