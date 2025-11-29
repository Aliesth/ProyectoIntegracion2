#!/usr/bin/env bash
# Termina el script si un comando falla
set -e 

echo "Corriendo Migraciones..."
# Ejecuta migraciones, usando la variable de entorno DATABASE_URL
python manage.py migrate

echo "Iniciando Gunicorn..."
# Inicia el servidor, ahora que las migraciones terminaron
gunicorn feriavirtual.wsgi:application