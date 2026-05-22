from django.db import models
from persons.models import Person
# Create your models here.


class Employee(Person):
    perfil = models.CharField('Perfil', max_length=50)
    position = models.CharField('Cargo', max_length=50)
    birth_date = models.DateField('Data de nascimento')
    hire_date = models.DateField('Data de contratação')
    is_active = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'
        ordering = ['person_ptr_id']

    def __str__(self):
        return super().__str__()
