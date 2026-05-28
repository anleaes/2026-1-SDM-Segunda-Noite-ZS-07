from django.db import models

# Create your models here.

class Specie(models.Model):
    name = models.CharField('Nome', max_length=200, null=False, blank=False)

    class Meta:
        verbose_name = 'Especie'
        verbose_name_plural = 'Especies'
        ordering =['id']

    def __str__(self):
        return f'{self.name}'