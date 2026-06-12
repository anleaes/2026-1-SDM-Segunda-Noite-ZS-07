from urllib import request

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from io import BytesIO
from .models import Adoption
from .serializer import (
    AdoptionCreateSerializer,
    AdoptionStaffSerializer,
    AdoptionStatusSerializer,
    AdoptionMySerializer,
)
from adoptionterm.models import Adoptionterm


class AdoptionViewSet(viewsets.ModelViewSet):
    queryset = Adoption.objects.all()
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_serializer_class(self):
        if self.action == 'create':
            return AdoptionCreateSerializer
        if self.action == 'partial_update':
            return AdoptionStatusSerializer
        if self.action == 'minhas':
            return AdoptionMySerializer
        return AdoptionStaffSerializer

    def get_permissions(self):
        if self.action in ['create', 'minhas']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(adopter=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_status = instance.status

        serializer = AdoptionStatusSerializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        new_status = serializer.instance.status
        if old_status != 'approved' and new_status == 'approved':
            animal = serializer.instance.animal
            animal.adopted = True
            animal.save()
            self._generate_term(serializer.instance)

        return Response(serializer.data)

    def _generate_term(self, adoption):
        if hasattr(adoption, 'adoption_term'):
            return

        adopter = adoption.adopter
        animal = adoption.animal

        sex_label = 'Macho' if animal.sex == 'M' else 'Fêmea'
        size_label = {'P': 'Pequeno porte', 'M': 'Médio porte',
                      'G': 'Grande porte'}.get(animal.size, '-')
        sterilized_label = 'Sim' if animal.sterilized else 'Não'

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        p.setFont('Helvetica-Bold', 16)
        p.drawCentredString(width / 2, height - 60, 'Termo de Adoção')

        y = height - 120

        def linha(texto, bold=False):
            nonlocal y
            p.setFont('Helvetica-Bold' if bold else 'Helvetica', 12)
            p.drawString(72, y, texto)
            y -= 22

        linha('DADOS DO ADOTANTE', bold=True)
        linha(f'Nome: {adopter.get_full_name() or adopter.username}')
        linha(f'E-mail: {adopter.email}')

        y -= 10
        linha('DADOS DO ANIMAL', bold=True)
        linha(f'Nome: {animal.name}')
        linha(f'Raça: {animal.breed}')
        linha(f'Sexo: {sex_label}')
        linha(f'Tamanho: {size_label}')
        linha(f'Cor: {animal.color}')
        linha(f'Castrado: {sterilized_label}')
        linha(
            f'Data de nascimento: {animal.birth_date.strftime("%d/%m/%Y") if animal.birth_date else "-"}')

        y -= 10
        linha('DECLARAÇÃO', bold=True)
        p.setFont('Helvetica', 11)
        texto = (
            'Ao retirar o animal descrito acima, o adotante declara estar ciente de suas '
            'responsabilidades, comprometendo-se a oferecer alimentação adequada, abrigo, '
            'cuidados veterinários e um ambiente seguro e afetuoso.'
        )
        for t in simpleSplit(texto, 'Helvetica', 11, width - 144):
            p.drawString(72, y, t)
            y -= 18

        y -= 20
        p.setFont('Helvetica', 12)
        linha(f'Data da adoção: {adoption.submitted_at.strftime("%d/%m/%Y")}')

        y -= 30
        p.drawString(
            72, y, 'Assinatura do adotante: ___________________________________')

        p.showPage()
        p.save()
        buffer.seek(0)

        Adoptionterm.objects.create(
            adoption=adoption,
            document=ContentFile(
                buffer.read(), name=f'termo_{adoption.id}.pdf'),
        )

    @action(
        detail=False,
        methods=['get'],
        url_path='minhas',
        permission_classes=[IsAuthenticated],
        authentication_classes=[TokenAuthentication, SessionAuthentication],
    )
    def minhas(self, request):
        queryset = Adoption.objects.filter(
            adopter=request.user).select_related('animal', 'adoption_term')
        serializer = AdoptionMySerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


@login_required
def adoption_form_page(request, animal_id):
    return render(request, 'adoptions/adoption_form.html', {
        'animal_id': animal_id
    })


@login_required
def my_requests_page(request):
    return render(request, 'adoptions/my_requests.html')


@user_passes_test(lambda user: user.is_staff)
def adoption_requests_panel(request):
    return render(request, 'adoptions/admin_requests.html')
