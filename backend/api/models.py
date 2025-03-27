from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Usuario(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name="usuario_groups",  # Cambiamos el related_name para evitar conflicto
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="usuario_permissions",  # Cambiamos el related_name para evitar conflicto
        blank=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.groups.exists():  # Si el usuario no tiene grupo, asignar "user" por defecto
            user_group, _ = Group.objects.get_or_create(name="user")
            self.groups.add(user_group)


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # <--- Este campo

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.username}"
