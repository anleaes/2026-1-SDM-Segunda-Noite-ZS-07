from django.db import models
from django.conf import settings
from animals.models import Animal


class Adoption(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovada'),
        ('rejected', 'Rejeitada'),
    ]

    # Controle
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    adopter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adoptions'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')

    # Dados pessoais
    full_name = models.CharField(max_length=200)
    cpf = models.CharField(max_length=11)
    birth_date = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=200, blank=True)
    occupation = models.CharField(max_length=200, blank=True)

    # Endereço
    cep = models.CharField(max_length=8)
    street = models.CharField(max_length=200)
    number = models.CharField(max_length=10)
    complement = models.CharField(max_length=100, blank=True)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)

    # Moradia
    housing_type = models.CharField(max_length=50)
    ownership_type = models.CharField(max_length=50)
    has_yard = models.BooleanField(default=False)
    yard_secured = models.BooleanField(default=False)
    residents_count = models.PositiveIntegerField()
    has_children = models.BooleanField(default=False)
    children_ages = models.CharField(max_length=100, blank=True)

    # Experiência com animais
    had_pets_before = models.BooleanField(default=False)
    currently_has_pets = models.BooleanField(default=False)
    current_pets_description = models.CharField(max_length=500, blank=True)

    # Motivação
    reason_for_adoption = models.TextField()
    caretaker = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Adoção'
        verbose_name_plural = 'Adoções'
        ordering = ['-submitted_at']

    def __str__(self):
        return f'Adoção #{self.id} — {self.full_name}'
