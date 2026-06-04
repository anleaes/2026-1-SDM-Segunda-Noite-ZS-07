from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.db import transaction
from django.contrib.auth.models import User
from .models import Adopter
from .serializer import AdopterSerializer

# Create your views here.
class AdopterViewSet(viewsets.ModelViewSet):
    queryset = Adopter.objects.all()
    serializer_class = AdopterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        data = request.data
        
        try:
            
            if User.objects.filter(username=data.get('username')).exists():
                return Response(
                    {"error": "Este nome de utilizador já está em uso."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():
                user = User.objects.create_user(
                    username=data.get('username'),
                    email=data.get('email'),
                    password=data.get('password'),
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name')
                )
                
                adopter = Adopter.objects.create(
                    user=user,
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    cpf=data.get('cpf'),
                    address=data.get('address'),
                    yard_security=data.get('yard_security', False),
                    addressComprove=data.get('addressComprove', False),
                    checkedData=data.get('checkedData', False),
                )
                
                serializer = self.get_serializer(adopter)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            print(f"======== ERRO NO CADASTRO DE CLIENTE: {str(e)} ========")
            return Response({"error": f"Falha no servidor: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def alterar_username(self, request, pk=None):
        adopter = self.get_object()
        user = adopter.user
        
        if not user:
            return Response({"error": "Este adotante não possui um usuário de login vinculado."}, status=status.HTTP_400_BAD_REQUEST)
            
        novo_username = request.data.get('username')
        if not novo_username:
            return Response({"error": "O novo nome de usuário não foi informado."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=novo_username).exclude(id=user.id).exists():
            return Response({"error": "Este nome de usuário já está em uso por outra pessoa."}, status=status.HTTP_400_BAD_REQUEST)
            
        user.username = novo_username
        user.save()
        return Response({"status": "Nome de usuário atualizado com sucesso!"})

    @action(detail=True, methods=['patch'])
    def alterar_senha(self, request, pk=None):
        if not request.user.is_superuser:
            return Response({"error": "Apenas administradores podem alterar senhas de clientes."}, status=status.HTTP_403_FORBIDDEN)
            
        adopter = self.get_object()
        user = adopter.user
        
        if not user:
            return Response({"error": "Este adotante não possui um usuário de login vinculado."}, status=status.HTTP_400_BAD_REQUEST)
            
        nova_senha = request.data.get('new_password')
        if not nova_senha:
            return Response({"error": "Nova senha não fornecida."}, status=status.HTTP_400_BAD_REQUEST)
            
        user.set_password(nova_senha)
        user.save()
        return Response({"status": "Senha do cliente atualizada com sucesso!"})