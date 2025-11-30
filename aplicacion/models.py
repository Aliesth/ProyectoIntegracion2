from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


class Rol(models.TextChoices):
    #ADMINISTRADOR = 'Administrador', _('administrador')
    productor = 'productor', _('productor') # Cambiado a 'Productor' según tu select
    cliente = 'cliente', _('cliente')
    #TRANSPORTISTA = 'TRANSPORTISTA', _('Transportista')
    #CONSULTOR = 'CONSULTOR', _('Consultor')


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
    imagen = models.ImageField(upload_to='frutas/', null=True, blank=True)
    marca=models.CharField(max_length=300)
    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        # Redirige a la lista después de crear/actualizar
        return reverse('productos')


    # 1. MODELO PEDIDO (Encabezado)


class Pedido(models.Model):
    # --- CAMPOS BASE ---
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # --- DEFINICIONES DE OPCIONES ---
    TIPO_ENVIO_CHOICES = [
        ('Nacional', 'Nacional'),
        ('Internacional', 'Internacional'),
    ]
    
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Bodega', 'En Bodega'),
        ('En Transporte', 'En Transporte'),
        ('Completado', 'Completado'),
    ]
    
    # --- CAMPOS DE ENVÍO Y ESTADO ---
    
    # 1. Dirección de Envío
    direccion_envio = models.CharField(
        max_length=500, 
        verbose_name='Dirección de Envío',
        default='Dirección pendiente de registro' 
    )
    
    # 2. Tipo de Envío
    tipo_envio = models.CharField(
        max_length=15, 
        choices=TIPO_ENVIO_CHOICES, 
        default='Nacional',
        verbose_name='Tipo de Envío'
    )

    # 3. Estado del Pedido
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='Pendiente', 
        verbose_name='Estado del Pedido'
    )
    
    def __str__(self):
        return f"Pedido #{self.id} de {self.usuario.username} ({self.estado})"
    
class DetallePedido(models.Model):
    pedido = models.ForeignKey('Pedido', related_name='detalles', on_delete=models.CASCADE) 
    
    #Si Fruta está definida antes, usamos Fruta. Si no, usamos 'Fruta'.
    fruta = models.ForeignKey('Fruta', on_delete=models.SET_NULL, null=True) 
    
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2) 
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        #Proteger contra objetos eliminados (NoneType error)
        fruta_nombre = self.fruta.nombre if self.fruta else "Producto Eliminado"
        
        # Proteger contra la eliminación del Pedido (menos probable con CASCADE)
        pedido_id = self.pedido.id if self.pedido else "N/A"
        
        return f"{self.cantidad} x {fruta_nombre} en Pedido #{pedido_id}"

class Contrato(models.Model):
    nombre_transporte = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.nombre_transporte} ({self.fecha_inicio} - {self.fecha_termino})"