from .models import Vaccine
from rest_framework import serializers

class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = '__all__'