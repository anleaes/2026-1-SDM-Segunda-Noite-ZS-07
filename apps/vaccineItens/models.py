from django.db import models
from vaccines.models import Vaccine
from vaccination.models import Vaccination


# Create your models here.
class VaccineItem(models.Model):
    expiration_date = models.DateField('Data de Validade')
    dosage = models.CharField('Dosagem', max_length=100)
    vaccination = models.ForeignKey(Vaccination, on_delete=models.CASCADE)
    vaccines = models.ForeignKey(Vaccine, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Item de Vacina'
        verbose_name_plural = 'Itens de Vacina'
        ordering = ['id']

    def __str__(self):
        return f"{self.vaccines} - {self.expiration_date}"
