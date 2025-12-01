# aplicacion/carrito.py

from decimal import Decimal
from django.conf import settings
from aplicacion.models import Fruta 
# ... (otras partes de la clase Cart)

def __iter__(self):
        """
        Itera sobre los ítems del carrito y obtiene los objetos Fruta de la BD.
        Maneja errores si la Fruta ya no existe en la BD.
        """
        fruta_ids = self.cart.keys()
        
        # 1. Obtener todos los objetos Fruta que existen en la BD
        frutas_objects = Fruta.objects.filter(id__in=fruta_ids)
        
        # Crear un mapa {id_fruta: objeto_fruta} para búsqueda rápida
        frutas_map = {str(fruta.id): fruta for fruta in frutas_objects}
        
        cart = self.cart.copy()
        
        for fruta_id in list(cart.keys()): # Iterar sobre una lista de IDs
            if fruta_id not in frutas_map:
                # 💡 CORRECCIÓN: Si la fruta se eliminó de la BD, la quitamos del carrito de sesión.
                del cart[fruta_id]
                self.remove(Fruta(id=fruta_id)) # Llama a remove para guardar el cambio en sesión
                continue 

            item = cart[fruta_id]
            item['fruta'] = frutas_map[fruta_id] # Asigna el objeto Fruta
            
            # 💡 CORRECCIÓN: Manejar errores de conversión a Decimal
            try:
                # Asegura que item['price'] es una cadena de número antes de convertir
                price_str = item.get('price', '0')
                if price_str is None or price_str == '':
                    price_str = '0'
                    
                item['price'] = Decimal(price_str)
            except:
                # Si falla la conversión (raro, pero posible), asumimos 0
                item['price'] = Decimal('0')
                
            item['total_price'] = item['price'] * item['quantity']
            
            yield item

# ... (otras partes de la clase Cart)