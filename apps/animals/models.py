from django.db import models
from breeds.models import Breed
from characteristics.models import Characteristic

# Create your models here.
class Animal(models.Model):
    id_animal = models.AutoField('ID do Animal', primary_key= True, null=False, editable=False, unique=True)
    name = models.CharField('Nome', null=False, max_length=100)
    birth_date = models.DateField('Data de Nascimento')
    sex = models.CharField('Sexo', max_length=10, null=False, choices=[
        ('M', 'Macho'),
        ('F', 'Femea'),
    ])
    size = models.CharField('Tamanho', max_length=20, null=False, choices=[
        ('P', 'Pequeno porte'),
        ('M', 'Médio porte'),
        ('G', 'Grande porte'),
    ])
    color = models.CharField('Cor', max_length=50)
    sterilized = models.BooleanField('Castrado', null=False, default=False, choices=[
        (True, 'Castrado'),
        (False, 'Não castrado'),
        ])
    listedAt = models.DateField('Data de Listagem')
    adopted = models.BooleanField('Adotado', null=False, default=False, choices=[
        (True, 'Adotado'),
        (False, 'Para adoção'),
        ])
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    characteristic = models.ManyToManyField(Characteristic, verbose_name='Caracteristicas')
    
    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animais'
        ordering =['id_animal']

    def __str__(self):
        return f'{self.name}'