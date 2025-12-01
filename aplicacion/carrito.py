from decimal import Decimal
from django.conf import settings
from aplicacion.models import Fruta


class Cart:
    """
    Clase para gestionar el carrito almacenado en la sesión.
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, fruta, quantity=1, override_quantity=False):
        """
        Añade un producto al carrito o actualiza su cantidad.
        """
        fruta_id = str(fruta.id)

        if fruta_id not in self.cart:
            self.cart[fruta_id] = {
                'quantity': 0,
                'price': str(fruta.precio)
            }

        if override_quantity:
            self.cart[fruta_id]['quantity'] = quantity
        else:
            self.cart[fruta_id]['quantity'] += quantity

        self.save()

    def save(self):
        """
        Marca la sesión como modificada.
        """
        self.session.modified = True

    def remove(self, fruta):
        fruta_id = str(fruta.id)

        if fruta_id in self.cart:
            del self.cart[fruta_id]
            self.save()

    def __iter__(self):
        """
        Itera sobre los ítems del carrito y obtiene los objetos Fruta reales.
        Si un producto ya no existe en la BD, se elimina del carrito.
        """
        fruta_ids = list(self.cart.keys())

        # Query a BD para obtener frutas existentes
        frutas = Fruta.objects.filter(id__in=fruta_ids)

        # IDs válidos (existen en BD)
        ids_validos = set(str(f.id) for f in frutas)

        # Eliminar productos que ya no existen
        for fruta_id in fruta_ids:
            if fruta_id not in ids_validos:
                del self.cart[fruta_id]
                self.save()

        # Copiamos el carrito para no modificar el original mientras iteramos
        cart = self.cart.copy()

        # Asignamos el objeto Fruta real
        for fruta in frutas:
            cart[str(fruta.id)]['fruta'] = fruta

        # Convertimos a Decimal y calculamos total
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Retorna la cantidad total de ítems (sumatoria de cantidades).
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calcula el total del carrito de forma segura.
        """
        total = Decimal('0.0')
        for item in self:
            total += item['total_price']
        return total

    def clear(self):
        """
        Vacía el carrito de la sesión.
        """
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()
