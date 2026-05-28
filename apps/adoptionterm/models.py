from django.db import models
from adoptions.models import Adoption

# Create your models here.

class Adoptionterm(models.Model):
    number = models.AutoField('Número', primary_key= True, blank=False, null=False, editable=False, unique=True)
    adopted_at = models.DateTimeField('Data da Adoção', auto_now_add=True, blank=False, null=False, editable=False)
    document = models.FileField('Documento', upload_to='docs', null=False, blank=False)
    adoption = models.OneToOneField(Adoption, on_delete=models.CASCADE, related_name='adoption_term')

    class Meta:
        verbose_name = 'Termo de Adocao'
        verbose_name_plural = 'Termos de Adocao'
        ordering = ['number']

    def __str__(self):
        return f'{self.number}'