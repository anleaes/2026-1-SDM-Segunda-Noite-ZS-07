from .models import Adopter
from rest_framework import serializers

class AdopterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adopter
        fields = '__all__'