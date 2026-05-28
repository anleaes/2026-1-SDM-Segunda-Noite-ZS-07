from .models import Specie
from rest_framework import serializers

class SpecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specie
        fields = '__all__'