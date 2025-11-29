# aplicacion/migrations/XXXX_auto_setup_roles.py

from django.db import migrations
# No necesitamos importar Group y Rol directamente aquí, ya que usamos apps.get_model

# Importa tu modelo de Rol para obtener las etiquetas (Asegúrate de que esta ruta sea correcta)
from aplicacion.models import Rol 

def create_initial_groups(apps, schema_editor):
    """Crea los grupos de permisos y asigna todos los permisos al grupo Administrador."""
    
    # Obtener los modelos de forma segura para las migraciones
    Group = apps.get_model('auth', 'Group') 
    Permission = apps.get_model('auth', 'Permission')
    
    # 1. CREAR TODOS LOS GRUPOS BÁSICOS
    for role_key, role_label in Rol.choices:
        Group.objects.get_or_create(name=role_key)
        
    # 2. CONFIGURAR PERMISOS PARA EL GRUPO ADMINISTRADOR
    
    # Obtener o crear el grupo de Administradores
    admin_group, created = Group.objects.get_or_create(name=Rol.ADMINISTRADOR.value)
    
    # Obtener todos los permisos disponibles en la BD
    all_permissions = Permission.objects.all()
    
    # Asignar todos los permisos al grupo Admin
    admin_group.permissions.set(all_permissions)


def reverse_initial_groups(apps, schema_editor):
    """Elimina los grupos en caso de que se revierta la migración."""
    Group = apps.get_model('auth', 'Group')
    
    # Elimina los grupos creados
    for role_key, role_label in Rol.choices:
        try:
            Group.objects.get(name=role_key).delete()
        except Group.DoesNotExist:
            pass


class Migration(migrations.Migration):

    dependencies = [
        # Asegúrate de que esta dependencia sea la migración anterior de tu app
        ('aplicacion', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(create_initial_groups, reverse_initial_groups),
    ]