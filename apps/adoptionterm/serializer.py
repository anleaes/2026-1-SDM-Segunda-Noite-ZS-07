from .models import Adoptionterm
from rest_framework import serializers


class AdoptiontermSerializer(serializers.ModelSerializer):
    document = serializers.SerializerMethodField()

    class Meta:
        model = Adoptionterm
        fields = ['number', 'adopted_at', 'document', 'adoption']

    def get_document(self, obj):
        request = self.context.get('request')
        if obj.document and request:
            return request.build_absolute_uri(obj.document.url)
        return obj.document.url if obj.document else None
