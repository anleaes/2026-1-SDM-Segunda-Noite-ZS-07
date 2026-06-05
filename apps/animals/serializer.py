from .models import Animal
from vaccines.models import Vaccine
from vaccination.models import Vaccination
from vaccineItens.models import VaccineItem
from rest_framework import serializers

class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = ['name', 'description','years_prevention']

class VaccineItemSerializer(serializers.ModelSerializer):
    # 'vaccines' é o nome da FK que está no seu diagrama
    vaccine_info = VaccineSerializer(source='vaccines', read_only=True)

    class Meta:
        model = VaccineItem # Ajuste para o nome do seu model
        fields = ['dosage', 'vaccine_info']

class VaccinationSerializer(serializers.ModelSerializer):
    # O Django usa o sufixo _set por padrão para relações reversas. 
    # Se você colocou um related_name no model, use ele no source.
    itens = VaccineItemSerializer(source='vaccineitem_set', many=True, read_only=True)

    class Meta:
        model = Vaccination
        fields = ['vaccinatedAt', 'weight_at', 'itens']

class AnimalSerializer(serializers.ModelSerializer):
    breed = serializers.StringRelatedField()
    characteristic = serializers.StringRelatedField(many=True)
    species = serializers.StringRelatedField(source='breed.specie', read_only=True)
    vaccine_history = VaccinationSerializer(source='vaccination_set', many=True, read_only=True)
    class Meta:
        model = Animal
        fields = '__all__'
