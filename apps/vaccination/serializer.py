from .models import Vaccination
from rest_framework import serializers

class VaccinationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vaccination
		
