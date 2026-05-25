from django.db import models
from adopters.models import Adopter
from employees.models import Employee
from animals.models import Animal

# Create your models here.

class Adoption(models.Model):
    submitedAt = models.DateTimeField(auto_now_add=True)
    status = models.CharField('Status da adoção', max_length=10, null=False, blank=False, default='Pendente',choices=[
        ('Pendente', 'Pendente'),
        ('Aprovada', 'Aprovada'),
        ('Rejeitada', 'Rejeitada'),
        ('Finalizada', 'Finalizada'),
    ])
    lastAnswer = models.DateTimeField('Última resposta', null=True, blank=True, default=0.0)
    adopter = models.ForeignKey(Adopter, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Adocao'
        verbose_name_plural = 'Adocoes'
        ordering =['id']

    def __str__(self):
        return f'{self.id}'