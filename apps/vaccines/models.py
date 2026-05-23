from django.db import models

# Create your models here.
class Vaccine(models.Model):
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', null=True, blank=True)
    years_prevention = models.FloatField('Anos de Prevenção', null=True, blank=True, default=1)
    manufacturer = models.CharField('Fabricante', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Vacina'
        verbose_name_plural = 'Vacinas'
        ordering =['id']

    def __str__(self):
        return f'{self.name}'