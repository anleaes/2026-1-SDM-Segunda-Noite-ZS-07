from django import forms
from .models import Animal

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = [
            'name', 'birth_date', 'sex', 'size', 'color', 
            'listedAt', 'photo', 'breed', 'sterilized',
            'adopted', 'characteristic'
        ]
        
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'listedAt': forms.DateInput(attrs={'type': 'date'}),
        }