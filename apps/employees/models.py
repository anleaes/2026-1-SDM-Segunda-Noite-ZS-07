from django.db import models
from persons.models import Person
# Create your models here.


class Employee(Person):
    perfil = models.CharField('Perfil', max_length=15, default='User', null=False, blank=False, choices=[
        ('Admin', 'Administrador'),
        ('Mod', 'Moderador'),
        ('User', 'Usuário')
    ])
    position = models.CharField('Cargo', max_length=200, null=False, blank=False)
    birth_date = models.DateField('Data de nascimento', null=False, blank=True)
    hire_date = models.DateField('Data da contratação', null=False, blank=False)
    is_active = models.BooleanField('Está Ativo?', default=True, null=False, choices=[
        (True, 'Ativo'),
        (False, 'Desativado')
    ])

    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'
        ordering = ['person_ptr_id']

    def __str__(self):
        return super().__str__()
