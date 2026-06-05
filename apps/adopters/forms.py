from django import forms
from .models import Adopter

class AdopterForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label='Usuário', required=True)
    email = forms.EmailField(label='E-mail', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Senha', required=True)

    class Meta:
        model = Adopter
        fields = [
            'username', 'email', 'first_name', 'last_name','password', 'cpf', 
            'address', 'yard_security', 'addressComprove', 'checkedData' 
        ]