from rest_framework import serializers
from .models import Adoption
from adoptionterm.serializer import AdoptiontermSerializer


class AdoptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        exclude = ['adopter', 'status', 'submitted_at']

    def validate_animal(self, value):
        if value.adopted:
            raise serializers.ValidationError('Este animal já foi adotado.')
        return value


class AdoptionStaffSerializer(serializers.ModelSerializer):
    animal_name = serializers.CharField(source='animal.name', read_only=True)

    class Meta:
        model = Adoption
        fields = '__all__'


class AdoptionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = ['status']


class AdoptionMySerializer(serializers.ModelSerializer):
    animal_name = serializers.CharField(source='animal.name', read_only=True)
    adoption_term = AdoptiontermSerializer(read_only=True)

    class Meta:
        model = Adoption
        fields = ['id', 'submitted_at', 'status',
                  'animal', 'animal_name', 'adoption_term']
