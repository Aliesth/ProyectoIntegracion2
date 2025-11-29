#!/usr/bin/env bash
set -e 

echo "Corriendo Migraciones..."
python manage.py migrate

echo "Iniciando Gunicorn..."
# 1. Aseguramos que la carpeta raíz esté en la ruta de Python
export PYTHONPATH=$PWD:$PYTHONPATH
# 2. Corremos Gunicorn usando el nombre exacto del módulo
gunicorn FeriaVirtual.wsgi:application