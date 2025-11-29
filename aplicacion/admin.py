from django.contrib import admin
from .models import Pedido, DetallePedido, Fruta, Contrato, Perfil

admin.site.register(Contrato)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Fruta)
admin.site.register(Perfil)