from django import forms
from .models import Vaccination

class VaccinationsForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = [
            'vaccinatedAt', 'weight_at',
            'animal', 'employee',
        ]
    