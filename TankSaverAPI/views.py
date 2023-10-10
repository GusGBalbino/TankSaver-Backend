from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from TankSaverAPI import models
from .api.serializer import CompraSerializer, PostoSerializer
from django.http import Http404

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        senha = request.data.get("senha")

        posto = models.Posto.objects.filter(email=email).first()

        if posto and posto.senha == senha:  # Por enquanto, comparando senhas em texto plano
            refresh = RefreshToken.for_user(posto)
            access_token = str(refresh.access_token)
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)

        return Response({"Erro": "Login inválido"}, status=status.HTTP_401_UNAUTHORIZED)
    
class CompraCreateView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = request.data
        data['posto'] = request.user.id # Atribui o posto logado ao pedido de compra
        
        serializer = CompraSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
