from django.db import models

# Create your models here.
class Characteristic(models.Model):
    name = models.CharField('Nome', max_length=100, null=False, blank=False)
    description = models.TextField('Descrição', blank=True)
    is_positive = models.BooleanField('Positiva', default=True)

    class Meta:
        verbose_name = 'Caracteristica'
        verbose_name_plural = 'Caracteristicas'
        ordering =['id']

    def __str__(self):
        return f'{self.name}'