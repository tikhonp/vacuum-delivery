from rest_framework import serializers
from delivaryapp.models import Orders


class SingleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
