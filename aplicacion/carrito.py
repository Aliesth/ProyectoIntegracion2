from decimal import Decimal
from django.conf import settings
from aplicacion.models import Fruta # Importamos tu modelo Fruta


class Cart:
    """
    Una clase simple para gestionar el carrito de compras, 
    almacenado en la sesión del usuario.
    """
    def __init__(self, request):
        """
        Inicializa el carrito.
        """
        self.session = request.session
        # Intenta obtener el carrito de la sesión. Si no existe, crea un diccionario vacío.
        cart = self.session.get(settings.CART_SESSION_ID) 
        if not cart:
            # Guarda un carrito vacío en la sesión
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, fruta, quantity=1, override_quantity=False):
        """
        Añade un producto al carrito o actualiza su cantidad.
        """
        fruta_id = str(fruta.id)
        
        # Si la fruta no está en el carrito, la inicializamos
        if fruta_id not in self.cart:
            self.cart[fruta_id] = {
                'quantity': 0,
                # Usamos 'precio' para coincidir con tu modelo Fruta
                'price': str(fruta.precio) 
            }
            
        if override_quantity:
            self.cart[fruta_id]['quantity'] = quantity
        else:
            self.cart[fruta_id]['quantity'] += quantity
        
        self.save()

    def save(self):
        """
        Marca la sesión como 'modificada' para asegurar que se guarde.
        """
        self.session.modified = True

    def remove(self, fruta):
        """
        Elimina la fruta del carrito.
        """
        fruta_id = str(fruta.id)
        if fruta_id in self.cart:
            del self.cart[fruta_id]
            self.save()

    def __iter__(self):
        """
        Itera sobre los ítems del carrito y obtiene los objetos Fruta de la BD.
        """
        fruta_ids = self.cart.keys()
        # Obtener los objetos Fruta y convertirlos en un diccionario
        frutas = Fruta.objects.filter(id__in=fruta_ids)
        cart = self.cart.copy()
        
        for fruta in frutas:
            cart[str(fruta.id)]['fruta'] = fruta # Añade el objeto Fruta al diccionario del item

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Retorna la cantidad total de ítems en el carrito.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calcula el costo total de los artículos en el carrito.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Vacía el carrito de la sesión.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()