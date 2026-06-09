from .models import Employee
from rest_framework import serializers

class EmployeeSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Employee
        fields = '__all__'

    def get_role(self, obj):
        if obj.user:
            if obj.user.is_superuser and obj.user.is_staff:
                return 'Administrador'
            elif obj.user.is_staff:
                return 'Moderador'
        return 'user'