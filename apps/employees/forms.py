from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label='Usuário', required=True)
    email = forms.EmailField(label='E-mail', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Senha', required=True)

    class Meta:
        model = Employee

        fields = [
            'username', 'email','first_name',
            'last_name', 'birth_date', 'cpf',
            'password', 'position', 'hire_date'
        ]

        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }

        exclude = ()