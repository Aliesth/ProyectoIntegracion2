from django.contrib import admin
from .models import PedidosRealizados, DetallePedido, Fruta, Contrato, Perfil,Pedidos

admin.site.register(Contrato)
admin.site.register(PedidosRealizados)
admin.site.register(Pedidos)
admin.site.register(DetallePedido)
admin.site.register(Fruta)
admin.site.register(Perfil)