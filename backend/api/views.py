from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UsuarioSerializer, LoginSerializer, UsuarioTokenSerializer
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class RegistroView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = UsuarioTokenSerializer(user).data
            return Response(token, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token = UsuarioTokenSerializer(user).data
                return Response(token, status=status.HTTP_200_OK)
            return Response({"error": "Credenciales incorrectas"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Producto, Pedido
from .serializers import ProductoSerializer, PedidoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]  # Protegemos con JWT
