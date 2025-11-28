from django.db import models
from django.contrib.auth.models import User 
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import date

class Rol(models.TextChoices):
    ADMINISTRADOR = 'Administrador', _('administrador')
    productor = 'productor', _('productor') # Cambiado a 'Productor' según tu select
    cliente = 'cliente', _('cliente')
    TRANSPORTISTA = 'TRANSPORTISTA', _('Transportista')
    CONSULTOR = 'CONSULTOR', _('Consultor')


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.cliente,
        verbose_name='Rol del usuario'
    )

    def __str__(self):
        return f'{self.usuario.username} - {self.rol}'
    

class Fruta(models.Model):
    nombre=models.CharField(max_length=300)
    descripcion=models.TextField()
    precio=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField()
    #imagen=models.ImageField()
    marca=models.CharField(max_length=300)

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        # Redirige a la lista después de crear/actualizar
        return reverse('productos')


    # 1. MODELO PEDIDO (Encabezado)
class Pedido(models.Model):
    # Enlaza el pedido al usuario. ON_DELETE=models.CASCADE significa que si el usuario se borra, sus pedidos también.
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Podrías agregar un campo de estado (ej: 'Pendiente', 'Enviado', 'Completado')
    
    def __str__(self):
        return f"Pedido #{self.id} de {self.usuario.email}"

# 2. MODELO DETALLEPEDIDO (Línea de producto)
class DetallePedido(models.Model):
    # Enlaza el detalle a un pedido (si borras el pedido, se borran sus detalles)
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE) 
    # Enlaza la fruta, pero el precio es fijo al momento de la compra
    fruta = models.ForeignKey(Fruta, on_delete=models.SET_NULL, null=True) 
    
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2) # Precio de venta al momento del pedido
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.cantidad} x {self.fruta.nombre} en Pedido #{self.pedido.id}"
    

class Contrato(models.Model):
    nombre_transporte = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.nombre_transporte} ({self.fecha_inicio} - {self.fecha_termino})"