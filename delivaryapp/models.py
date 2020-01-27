from django.db import models
from django.contrib.auth.models import User
import datetime


class userplaces(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(("Date"), default=datetime.date.today)
    place = models.CharField(max_length=3)
    is_active = models.BooleanField(default=False)


class orders(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(("Date"), default=datetime.date.today)
    description = models.TextField()
    place = models.CharField(max_length=3)
    is_active = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    wuser = models.CharField(max_length=20, default='None')
