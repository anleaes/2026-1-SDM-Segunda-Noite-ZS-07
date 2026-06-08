from .models import Breed, Specie
from rest_framework import serializers

class BreedSerializer(serializers.ModelSerializer):
    specie = serializers.PrimaryKeyRelatedField(queryset=Specie.objects.all())
    class Meta:
        model = Breed
        fields = '__all__'