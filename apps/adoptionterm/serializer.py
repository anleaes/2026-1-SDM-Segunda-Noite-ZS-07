from .models import Adoptionterm
from rest_framework import serializers

class AdoptiontermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoptionterm
        fields = '__all__'