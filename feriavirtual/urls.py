from django.contrib import admin
from django.urls import path
from aplicacion import views
from aplicacion.views import CatalogoFrutasView, FrutaGestionListView, FrutaCreateView, FrutaUpdateView, FrutaDeleteView # Importaciones adicionales
from django.contrib.auth.decorators import user_passes_test # 👈 Importación NECESARIA
from django.conf.urls import handler404, handler500 
app_nanme = 'aplicacion'
# --- Define el decorador de rol para las CBV ---
# Lo definimos aquí porque el error estaba en este archivo.
productor_o_admin_required = user_passes_test(views.es_productor_o_admin, login_url='index')
admin_required = user_passes_test(views.es_administrador, login_url='index')
productor_required = user_passes_test(views.es_productor, login_url='index')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- Autenticación ---
    path('', views.login_usuario, name='login_usuario'), 
    path('register/', views.registrar_usuario, name='register'),
    path('home/', views.index, name='index'), 
    
    # --- Rutas de Catálogo Públicas (Cliente) ---
    # La ruta 'productos/' ahora usa el ListView
    path('productos/', CatalogoFrutasView.as_view(), name='productos'), 
    
    # La ruta 'catalogo/' original ahora se puede usar como la vista pública también
    path('catalogo/', CatalogoFrutasView.as_view(), name='catalogo_frutas'),
    
    # --- Rutas de Gestión del Catálogo (CRUD - Usuario Productor/Admin) ---
    
   
    
    path('catalogo/gestion/', productor_o_admin_required(views.FrutaGestionListView.as_view()), name='catalogo_gestion'),
    path('catalogo/gestion/crear/', productor_o_admin_required(views.FrutaCreateView.as_view()), name='fruta_crear'),
    path('catalogo/gestion/editar/<int:pk>/', admin_required(views.FrutaUpdateView.as_view()), name='fruta_editar'),
    path('catalogo/gestion/eliminar/<int:pk>/', admin_required(views.FrutaDeleteView.as_view()), name='fruta_eliminar'),
    
    # --- Otras Vistas Simples ---
    
    path('subastas/', views.subastas, name='subastas'),
    path('reportes/', views.reportes, name='reportes'),
    path('ventas/', views.ventas, name='ventas'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('add/<int:fruta_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    
    # URL 2: Vista para procesar la confirmación y crear el pedido
    path('confirmar-pedido/', views.confirmar_pedido, name='confirmar_pedido'),
    
    # URL 3: (Opcional) Página de éxito después de la compra
    path('pedido-exitoso/<int:pedido_id>/', views.pedido_exitoso, name='pedido_exitoso'),
    path('carrito/', views.mostrar_carrito, name='carrito'),
    # El <int:pedido_id> asegura que se pase el ID a la función pedido_exitoso.
    path('pedido-exitoso/<int:pedido_id>/', views.pedido_exitoso, name='pedido_exitoso'),
    
    # La vista de confirmación que llama a esta página (Pedido -> BD)
    path('confirmar-pedido/', views.confirmar_pedido, name='confirmar_pedido'),
    path('logout/', views.cerrar_sesion, name='logout'),

    
    path('contratos/', views.contrato_list, name='contrato_list'),
    path('gestion_contratos/', views.gestion_contratos, name='gestion_contratos'),
    path('contratos/editar/<int:id>/', views.contrato_editar, name='contrato_editar'),
    path('contratos/eliminar/<int:id>/', views.contrato_eliminar, name='contrato_eliminar'),
]