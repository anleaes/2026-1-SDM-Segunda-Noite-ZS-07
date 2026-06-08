from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .models import Adoption
from .serializer import (
    AdoptionCreateSerializer,
    AdoptionStaffSerializer,
    AdoptionStatusSerializer,
    AdoptionMySerializer,
)


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
        serializer = AdoptionStatusSerializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['get'],
        url_path='minhas',
        permission_classes=[IsAuthenticated],
        authentication_classes=[TokenAuthentication, SessionAuthentication],
    )
    def minhas(self, request):
        queryset = Adoption.objects.filter(adopter=request.user)
        serializer = AdoptionMySerializer(queryset, many=True)
        return Response(serializer.data)
