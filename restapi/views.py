from django.shortcuts import render
from delivaryapp.models import orders
from django.contrib.auth.models import User
from .serializers import ordersSerializer
from rest_framework import viewsets


class ordersViewSet(viewsets.ModelViewSet):
    queryset = orders.objects.filter(is_active=False, is_closed=False)
    serializer_class = ordersSerializer
