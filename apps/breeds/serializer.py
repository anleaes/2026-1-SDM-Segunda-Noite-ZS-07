from .models import Breed
from rest_framework import serializers

class BreedSerializer(serializers.ModelSerializer):
    specie = serializers.StringRelatedField()
    class Meta:
        model = Breed
        fields = '__all__'