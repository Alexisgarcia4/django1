from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

Usuario = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UsuarioTokenSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'token')

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
from rest_framework import serializers
from .models import Producto, Pedido

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    productos = ProductoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'
