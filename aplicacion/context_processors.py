from .utils import es_cliente, es_productor, puede_comprar 

def role_verifier(request):
    """Añade variables de rol/permiso al contexto de la plantilla."""
    
    # Si el usuario no está autenticado, devolvemos False para todas las variables
    if not request.user.is_authenticated:
        return {
            'es_cliente': False,
            'es_productor': False,
            'puede_comprar': False,
            'es_administrador': False,
        }

    return {
        # Estas variables estarán disponibles en TODOS tus archivos HTML
        'es_cliente': es_cliente(request.user),
        'es_productor': es_productor(request.user),
        'puede_comprar': puede_comprar(request.user),
        'es_administrador': request.user.is_superuser,
    }