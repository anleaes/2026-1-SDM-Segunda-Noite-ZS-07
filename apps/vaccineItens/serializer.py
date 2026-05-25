from .models import VaccineItem
from rest_framework import serializers


class VaccineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineItem
        
