from django.db import models

# Create your models here.

class Person(models.Model):
    register = models.AutoField('Registro', primary_key= True, null=False, editable=False, unique=True)
    registerAt = models.DateTimeField('Data do registro', auto_now_add=True, null=False, editable=False)
    first_name = models.CharField('Nome', max_length=50)
    last_name = models.CharField('Sobrenome', max_length=150)
    cpf = models.CharField('CPF', max_length=14, null=False, blank=False)

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering =['register']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'