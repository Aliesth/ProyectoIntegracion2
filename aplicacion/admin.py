from django.contrib import admin
from .models import PedidosRealizados, DetalledePedido, Fruta, Contrato, Perfil,Pedidos,DetallePedido

admin.site.register(Contrato)
admin.site.register(PedidosRealizados)
admin.site.register(Pedidos)
admin.site.register(DetalledePedido)
admin.site.register(Fruta)
admin.site.register(Perfil)
admin.site.register(DetallePedido)