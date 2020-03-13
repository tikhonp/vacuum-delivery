from rest_framework import serializers
from delivaryapp.models import orders
from django.contrib.auth.models import User


class ordersSerializer(serializers.ModelSerializer):
    class Meta:
        model = orders
        fields = ('id', 'author', 'date', 'description', 'place',
                  'is_active', 'is_closed', 'wuser')
