from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django import forms
from django.contrib.auth.models import Group
# Importaciones para las Class-Based Views
from django.views.generic import ListView, CreateView, UpdateView, DeleteView 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin 
# Importaciones de Modelos y Formularios
from .forms import FrutaForm, RegistroForm, ContratoForm
from .carrito import Cart
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Pedido, DetallePedido, Fruta, Contrato, Perfil
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from django.http import HttpResponse
# Asegúrate de importar los modelos correctos
from .models import PedidosRealizados, DetalledePedido, DetallePedido,Pedidos  
from django.contrib.admin.views.decorators import staff_member_required
# para de finir roles de usuario y usar decoradores

TASA_ADUANA = Decimal('0.20') # 20% de aduana para internacional
COSTO_BASE_ENVIO_NACIONAL = Decimal('5000.00') # Costo fijo para Chile
COSTO_BASE_ENVIO_INTERNACIONAL = Decimal('8000.00') # Costo fijo para otros países

def es_cliente(user):
    #verificar si es cliente
    return user.groups.filter(name='cliente').exists()

def es_productor(user):
    #verificar si es productor
    return user.groups.filter(name='productor').exists()

def es_administrador(user):
    #verificar si es cliente
    return user.groups.filter(name='Administrador').exists()
def es_productor_o_admin(user):
    return es_productor(user) or es_administrador(user)

def es_transportista(user):
    return user.groups.filter(name='TRANSPORTISTA').exists()
# ----------------------------------------------------------------------
# --- VISTAS DE GESTIÓN DE CATÁLOGO (CRUD - Fruta) ---
# ----------------------------------------------------------------------


class FrutaGestionListView(LoginRequiredMixin, ListView):
    """(R - READ) Muestra el panel de gestión del catálogo para editar/eliminar."""
    model = Fruta
    template_name = 'catalogo/fruta_gestion_list.html' 
    context_object_name = 'frutas_gestion'

class FrutaCreateView(LoginRequiredMixin, CreateView):
    """(C - CREATE) Vista para crear un nuevo producto (Fruta)."""
    model = Fruta
    form_class = FrutaForm # Usa la clase importada desde forms.py
    template_name = 'catalogo/fruta_form.html'
    success_url = reverse_lazy('catalogo_gestion') # Redirige al panel de gestión

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Añadir Nuevo Producto'
        return context

class FrutaUpdateView(LoginRequiredMixin, UpdateView):
    """(U - UPDATE) Vista para actualizar un producto existente (Fruta)."""
    model = Fruta
    form_class = FrutaForm
    template_name = 'catalogo/fruta_form.html'
    success_url = reverse_lazy('catalogo_gestion') # Redirige al panel de gestión

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Producto'
        return context

class FrutaDeleteView(LoginRequiredMixin, DeleteView):
    """(D - DELETE) Vista para eliminar un producto (Fruta) existente."""
    model = Fruta
    template_name = 'catalogo/fruta_confirm_delete.html' 
    success_url = reverse_lazy('catalogo_gestion') # Redirige al panel después de eliminar


# ----------------------------------------------------------------------
# --- VISTAS DE CATÁLOGO PÚBLICO Y PÁGINAS GENERALES ---
# ----------------------------------------------------------------------
login_required
class CatalogoFrutasView(ListView):
    """(R - READ) Muestra el catálogo público para los clientes."""
    model=Fruta
    template_name='catalogo/lista_frutas.html'
    context_object_name="frutas"
    paginate_by=12 

"""@login_required    
def index(request):
    return render(request, 'index.html') """
@login_required  
def index(request):
    
    context = {
        'es_administrador': es_administrador(request.user),
        # Puedes añadir otros roles si los necesitas en la misma vista
        'es_productor': es_productor(request.user), 
        'es_transportista': es_transportista(request.user),
    }
    
    return render(request, 'index.html', context)


login_required
def productos(request):
    context = {
        'es_administrador': es_administrador(request.user),
        # Puedes añadir otros roles si los necesitas en la misma vista
        # 'es_productor': es_productor(request.user), 
    }
    
    # Esta función puede eliminarse si la URL 'productos' apunta a CatalogoFrutasView
    return render(request, 'productos.html',context) 
    
def carrito(request):
    # Vista simple de página, ya no tiene lógica de sesión
    return render(request, 'carrito.html')

@require_POST
def eliminar_del_carrito(request, fruta_id):
    """Elimina completamente un producto del carrito de la sesión."""
    
    # 1. Obtener el objeto Fruta
    fruta = get_object_or_404(Fruta, id=fruta_id)
    
    # 2. Inicializar el carrito (carga desde la sesión)
    carrito = Cart(request)
    
    # 3. Llamar al método de eliminación de la clase Cart
    # Asumo que tu clase Cart tiene un método 'remove'
    carrito.remove(fruta)
    
    # 4. Redirigir de nuevo a la página del carrito
    return redirect('carrito')

@require_POST
def actualizar_carrito(request, fruta_id):
    """
    Actualiza la cantidad de una fruta en el carrito usando la acción
    enviada por el formulario (incrementar o decrementar).
    """
    
    fruta = get_object_or_404(Fruta, id=fruta_id)
    carrito = Cart(request)
    
    # Asegúrate de que la fruta esté en el carrito para evitar errores
    if str(fruta_id) not in carrito.cart:
        return redirect('carrito')

    # Determinar la acción y la cantidad actual
    action = request.POST.get('action') # Viene del botón (+ o -)

    if action == 'increment':
        # Intenta añadir +1. El método add de la clase Cart debe manejar la actualización.
        carrito.add(fruta=fruta, quantity=1, override_quantity=False) 
        
    elif action == 'decrement':
        # Si la cantidad actual es mayor que 1, decrementa en 1.
        if carrito.cart[str(fruta_id)]['quantity'] > 1:
            # Para decrementar, llamamos a 'add' con cantidad negativa.
            # (Esto requiere que el método add de tu clase Cart maneje cantidades negativas para restar)
            carrito.add(fruta=fruta, quantity=-1, override_quantity=False)
        else:
            # Si la cantidad es 1 y el usuario presiona '-', lo eliminamos.
            carrito.remove(fruta) # Asumiendo que existe el método remove
            
    return redirect('carrito')

def subastas(request):
    return render(request, 'subastas.html')

def reportes(request):
    return render(request, 'reportes.html')

def ventas(request):
    return render(request, 'ventas.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def mostrar_carrito(request):
    carrito = Cart(request)
    
    # 1. Obtener el subtotal de los productos
    # 🚨 CORRECCIÓN: Forzamos la conversión a Decimal para evitar errores de tipo. 🚨
    try:
        subtotal_sin_envio = Decimal(carrito.get_total_price())
    except TypeError:
        # Esto maneja si get_total_price devuelve None o algo que no se puede convertir
        subtotal_sin_envio = Decimal('0.00')

    # 2. DETERMINAR LA SELECCIÓN DE PAÍS (Lógica para capturar GET/POST correcta)
    if request.method == 'POST':
        tipo_envio_seleccionado = request.POST.get('pais', 'CL')
    else:
        tipo_envio_seleccionado = request.GET.get('pais', 'CL') 
        
    costo_envio = Decimal('0.00')
    costo_aduana = Decimal('0.00')
    total_final = subtotal_sin_envio
    
    # 3. LÓGICA DE CÁLCULO
    if subtotal_sin_envio > Decimal('0.00'): # Usamos subtotal_sin_envio para la comprobación
        
        if tipo_envio_seleccionado == 'CL':
            # Envío Nacional: Costo fijo
            costo_envio = COSTO_BASE_ENVIO_NACIONAL
            
        elif tipo_envio_seleccionado == 'OTRO':
            # Envío Internacional: Costo fijo más Aduana
            costo_envio = COSTO_BASE_ENVIO_INTERNACIONAL
            costo_aduana = subtotal_sin_envio * TASA_ADUANA
            
        # Calcular el total final
        total_final = subtotal_sin_envio + costo_envio + costo_aduana
        # Ahora que todas las variables son Decimals, la suma final es segura.

    context = {
        'carrito': carrito,
        'subtotal_sin_envio': subtotal_sin_envio,
        'costo_envio': costo_envio,
        'costo_aduana': costo_aduana,
        'total_final': total_final,
        'tipo_envio': tipo_envio_seleccionado, # Para mantener la selección en el <select>
    }
    
    return render(request, 'carrito.html', context)
# ----------------------------------------------------------------------
# --- VISTAS DE AUTENTICACIÓN ---
# ----------------------------------------------------------------------

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index') 
        return render(request, 'login.html', {
            'login_form': form, 
            'register_form': RegistroForm() 
        })
    else:
        return render(request, 'login.html', {
            'login_form': AuthenticationForm(), 
            'register_form': RegistroForm()
        })


def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST) 
        if form.is_valid():
            user_rol_name = form.cleaned_data.get('rolReg')
            try:
                with transaction.atomic():
                    user = form.save() 
                    Perfil.objects.create(usuario=user, rol=user_rol_name)
                    try:
                        grupo_django = Group.objects.get(name=user_rol_name)
                        user.groups.add(grupo_django)
                        print(f"✅ Usuario {user.username} asignado al grupo {user_rol_name}.")
                    except Group.DoesNotExist:
                        print(f"🛑 ADVERTENCIA: El Grupo '{user_rol_name}' no existe en Django. Asignación omitida.")
                        pass 
                    login(request, user)
                    return redirect('index') 
            except Exception as e:
                print(f"🛑 FALLO CRÍTICO DURANTE LA TRANSACCIÓN: {e}")
                form.add_error(None, "Ocurrió un error al crear el usuario. Por favor, inténtelo de nuevo.")
                
        return render(request, 'login.html', {
            'register_form': form, 
            'login_form': AuthenticationForm() 
        })
    else:
        return redirect('login_usuario')
def cerrar_sesion(request):
    """
    Función para cerrar la sesión del usuario actual.
    Utiliza la función logout de Django y redirige.
    """
    logout(request)
    # Redirige a la página de login
    return redirect('login_usuario')
    
@require_POST
def agregar_al_carrito(request, fruta_id):
    # Sólo usuarios registrados
    if not request.user.is_authenticated:
        return redirect('login_usuario') 
        
    carrito = Cart(request)
    fruta = get_object_or_404(Fruta, id=fruta_id)
    
    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except ValueError:
        cantidad = 1 # Usar 1 si la cantidad no es un número válido

    carrito.add(fruta=fruta, quantity=cantidad) 
    
    return redirect('catalogo_frutas')

@login_required
def confirmar_pedido(request):
    carrito = Cart(request)
    
    if not carrito:
        messages.error(request, "No puedes confirmar un pedido con el carrito vacío.")
        return redirect('carrito') 

    if request.method == 'POST':
        try:
            # Iniciamos la transacción aquí. Si algo falla dentro, se revierte.
            #with transaction.atomic():
                # 1. RECIBIR DATOS DEL FORMULARIO DE DIRECCIÓN
                direccion_recibida = request.POST.get('direccion_completa')
                pais_code = request.POST.get('pais')
                
                if not direccion_recibida or not pais_code:
                    messages.error(request, "Por favor, completa la dirección y el país de envío.")
                    return redirect('carrito')

                # 2. DETERMINAR EL TIPO DE ENVÍO Y COSTOS
                if pais_code == 'CL':
                    tipo_envio_final = 'Nacional'
                    costo_envio = COSTO_BASE_ENVIO_NACIONAL
                    costo_aduana = Decimal('0.00')
                else:
                    tipo_envio_final = 'Internacional'
                    subtotal_productos = carrito.get_total_price()
                    costo_envio = COSTO_BASE_ENVIO_INTERNACIONAL
                    costo_aduana = subtotal_productos * TASA_ADUANA
                
                # 3. RECALCULAR EL TOTAL FINAL
                total_a_cobrar = carrito.get_total_price() + costo_envio + costo_aduana
                
                # 4. CREAR EL PEDIDO (Encabezado)
                nuevo_pedido = Pedidos.objects.create(
                    usuario=request.user,
                    total_pedido=total_a_cobrar, 
                    direccion_envio=direccion_recibida,
                    tipo_envio=tipo_envio_final,
                    estado='Pendiente'

                )

                # 5. CREAR LOS DETALLES DEL PEDIDO y ACTUALIZAR EL STOCK
                for item_id, item_data in carrito.cart.items():
                    fruta = get_object_or_404(Fruta, id=item_id)
                    cantidad = Decimal(item_data['quantity'])
                    precio = Decimal(item_data['price'])  
                    
                    # 5a. Comprobar y DEDUCIR EL STOCK
                """if fruta.stock < cantidad:
                        # 🚨 ¡ERROR DE STOCK! Esto fuerza la reversión de la transacción.
                        messages.error(request, f"Stock insuficiente: Solo quedan {fruta.stock} unidades de {fruta.nombre}.")
                        raise ValueError(f"Stock insuficiente para {fruta.nombre}.") """
                    
                fruta.stock -= int(cantidad) # <-- Usamos int si stock es IntegerField
                fruta.save()
                    
                    # 5b. Guardar cada línea de detalle
                DetallePedido.objects.create(
                        pedido=nuevo_pedido,
                        fruta=fruta,
                        cantidad=int(cantidad),
                        precio_unitario=precio,
                        subtotal=(cantidad * precio)
                    )
                
                # 6. LIMPIAR EL CARRITO DE LA SESIÓN (Solo si la transacción fue exitosa)
                 

                messages.success(request, f"¡Pedido N°{nuevo_pedido.id} confirmado con éxito! Envío: {tipo_envio_final}.")
                carrito.clear()
                # 7. Redirigir a la página de éxito
                return redirect('pedido_exitoso', pedido_id=nuevo_pedido.id)
                #return redirect('index')
        except ValueError:
            # 🚨 Capturamos el ValueError (Stock Insuficiente) y redirigimos al carrito 🚨
            # El mensaje de error ya fue añadido en el Paso 5a
            return redirect('carrito')
            
        except Exception as e:
             # Captura cualquier otro error durante la transacción (ej. DB, etc.)
            messages.error(request, f"Ocurrió un error inesperado durante el checkout. Inténtalo de nuevo. Detalle: {e}")
            return redirect('carrito')

    # Si la petición no es POST, redirigimos al carrito
    return redirect('carrito')
@login_required
def pedido_exitoso(request, pedido_id):
    # 1. Obtiene el pedido o devuelve un error 404 si no existe
    pedido = get_object_or_404(Pedidos, id=pedido_id)
    
    # 2. Asegúrate de que el usuario que ve el pedido es el dueño (Seguridad)
    if pedido.usuario != request.user:
        return redirect('index') 

    # 3. Prepara los datos de contexto
    detalles_antiguos = pedido.detalles_antiguos.all() 
    
    # PASO CRÍTICO: Cálculo del desglose en Python 
    
    # A. Sumar el subtotal de todos los productos (total de ítems sin envío)
    # Usamos sum() sobre un generador para sumar los campos Decimal
    total_productos_acumulado = sum(detalle.subtotal for detalle in detalles_antiguos)

    # B. Calcular el Costo de Envío y Aduana por diferencia
    # total_guardado (en DB) - subtotal_productos (calculado ahora)
    costo_envio_final = pedido.total_pedido - total_productos_acumulado
    
    # Aseguramos que los valores no sean negativos si hay algún error de cálculo
    if costo_envio_final < Decimal('0.00'):
        costo_envio_final = Decimal('0.00')

    context = {
        'titulo': 'Pedido Confirmado',
        'pedido': pedido,
        'detalles': detalles_antiguos,
        # PASAMOS LAS VARIABLES AL CONTEXTO 
        'total_productos_acumulado': total_productos_acumulado,
        'costo_envio_final': costo_envio_final, 
    }
    
    # 4. Renderiza la plantilla
    return render(request, 'pedido_exitoso.html', context)

    """context = {
        'pedido': pedido,
        # Django te permite acceder a los DetallePedido usando el related_name='detalles'
        'detalles': pedido.detalles.all() 
    }
    
    # Asegúrate de crear este template: aplicacion/templates/pedido_exitoso.html
    return render(request, 'pedido_exitoso.html', context)"""


#Vista para contratos de transportes
def contrato_list(request):
    contratos = Contrato.objects.all()
    return render(request, 'contratos/contratos_list.html', {'contratos': contratos})

def gestion_contratos(request):
    form = ContratoForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Contrato agregado correctamente.')
            form = ContratoForm()  # limpiar el formulario
    contratos = Contrato.objects.all().order_by('-id')
    return render(request, 'contratos/gestion_contratos.html', {'form': form, 'contratos': contratos})

# Funciones vacías de ejemplo para futuras acciones
def contrato_editar(request, id):
    # Aquí se implementará la edición
    return redirect('gestion_contratos')

def contrato_eliminar(request, id):
    contrato = get_object_or_404(Contrato, id=id)
    contrato.delete()
    return redirect('gestion_contratos')






@staff_member_required
def vaciar_tablas_pedido(request):
    """
    Elimina todos los registros de Pedido y DetallePedido.
    
    Nota: Como DetallePedido usa on_delete=CASCADE al Pedido, 
    al eliminar Pedido, los detalles se borran automáticamente.
    """
    
    # Se eliminan los registros de Pedido. El borrado en cascada 
    # se encargará de DetallePedido.
    count_pedidos = PedidosRealizados.objects.all()
    
    # El resultado de .delete() es una tupla: (número_objetos_eliminados, {diccionario_de_counts})
    total_eliminado = count_pedidos
    
    mensaje = (
        f"🗑️ *¡Éxito!* La limpieza ha sido ejecutada."
        f"Se eliminaron *{total_eliminado}* registros de Pedido y sus líneas de detalle relacionadas."
        f"<br><br>Intente acceder a la tabla Pedido en el admin nuevamente."
    )
    
    return HttpResponse(mensaje)
