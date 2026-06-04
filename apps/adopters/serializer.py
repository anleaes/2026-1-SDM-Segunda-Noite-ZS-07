from .models import Adopter
from rest_framework import serializers

class AdopterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Adopter
        fields = '__all__'