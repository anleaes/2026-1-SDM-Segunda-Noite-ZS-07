from .models import Employee
from rest_framework import serializers

class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Employee
        fields = '__all__'