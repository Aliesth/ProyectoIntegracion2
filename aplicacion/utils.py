# En una carpeta de utilidades o en la parte superior de views.py

def es_cliente(user):
    """Retorna True si el usuario pertenece al grupo 'Cliente'."""
    # Comprueba si el usuario está autenticado y en el grupo
    return user.is_authenticated and user.groups.filter(name='Cliente').exists()

def es_productor(user):
    """Retorna True si el usuario pertenece al grupo 'Productor'."""
    return user.is_authenticated and user.groups.filter(name='Productor').exists()

def puede_comprar(user):
    """Retorna True si el usuario es Admin o Cliente."""
    return user.is_superuser or es_cliente(user)