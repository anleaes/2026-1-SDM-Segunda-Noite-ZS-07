from .models import Animal
from rest_framework import serializers

class AnimalSerializer(serializers.ModelSerializer):
    breed = serializers.StringRelatedField()
    characteristic = serializers.StringRelatedField(many=True)
    species = serializers.StringRelatedField(source='breed.specie', read_only=True)
    class Meta:
        model = Animal
        fields = '__all__'
