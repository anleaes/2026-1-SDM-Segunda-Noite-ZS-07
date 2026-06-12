from django import forms
from .models import Vaccine

class VaccinesForm(forms.ModelForm):
    class Meta:
        model = Vaccine
        fields = [
            'name', 'description',
            'years_prevention', 'manufacturer',
        ]
    