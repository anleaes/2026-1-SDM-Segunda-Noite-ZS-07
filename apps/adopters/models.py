from django.db import models
from persons.models import Person

# Create your models here.
class Adopter(Person):
    yard_security = models.BooleanField('Segurança do Jardim', null=False, choices=[
        (True, 'Seguro'),
        (False, 'Não seguro'),
    ])
    address = models.CharField('Endereco', max_length=200)
    addressComprove = models.BooleanField('Comprovante de Endereço', null=False, choices=[
        (True, 'Comprovado'),
        (False, 'Não comprovado'),
    ])
    checkedData = models.BooleanField('Dados Verificados', null=False, choices=[
        (True, 'Verificado'),
        (False, 'Não verificado'),
    ])

    class Meta:
        verbose_name = 'Adotante'
        verbose_name_plural = 'Adotantes'
        ordering =['id']

    def __str__(self):
        return super().__str__()