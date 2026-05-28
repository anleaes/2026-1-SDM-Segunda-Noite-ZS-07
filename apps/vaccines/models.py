from django.db import models

# Create your models here.
class Vaccine(models.Model):
    name = models.CharField('Nome', max_length=150, blank=False, null=False)
    description = models.TextField('Descrição', null=True, blank=True)
    years_prevention = models.FloatField('Anos de Prevenção', null=False, blank=False)
    manufacturer = models.CharField('Fabricante', max_length=150, null=False, blank=False)

    class Meta:
        verbose_name = 'Vacina'
        verbose_name_plural = 'Vacinas'
        ordering =['id']

    def __str__(self):
        return f'{self.name}'