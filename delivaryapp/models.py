from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class UserPlaces(models.Model):
    author = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True)
    date = models.DateField(("Date"), default=timezone.now)
    place = models.CharField(max_length=3, default=0)
    is_active = models.BooleanField(default=False)


class Orders(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateField(("Date"), default=timezone.now)
    description = models.TextField()
    place = models.CharField(max_length=3)
    is_active = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    wuser = models.CharField(max_length=20, default='None')
