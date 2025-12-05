from django.contrib import admin
from .models import Pedido, DetallePedido, Fruta, Contrato, Perfil,PedidosRealizados

admin.site.register(Contrato)
admin.site.register(PedidosRealizados)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Fruta)
admin.site.register(Perfil)