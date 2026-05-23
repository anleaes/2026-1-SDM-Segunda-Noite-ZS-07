from .models import Characteristic
from rest_framework import serializers

class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'
