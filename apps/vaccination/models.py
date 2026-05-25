from django.db import models
from animals.models import Animal
from employees.models import Employee

# Create your models here.
class Vaccination(models.Model):
	vaccinatedAt = models.DateField('Data de Vacinação')
	weight_at = models.FloatField('Peso na Vacinação', null=True, blank=True)
	animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
	employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)

	class Meta:
		verbose_name = 'Vacinação'
		verbose_name_plural = 'Vacinações'
		ordering = ['id']

	def __str__(self):
		return f"Vacinação {self.id} - {self.animal} em {self.vaccinatedAt}"
