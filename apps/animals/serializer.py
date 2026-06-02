from .models import Animal
from rest_framework import serializers

class AnimalSerializer(serializers.ModelSerializer):
    breed = serializers.StringRelatedField()
    characteristic = serializers.StringRelatedField(many=True)
    class Meta:
        model = Animal
        fields = '__all__'
