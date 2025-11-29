#!/usr/bin/env bash
set -e 

echo "Corriendo Migraciones..."
# Las migraciones se ejecutan desde la raíz.
python manage.py migrate

echo "Iniciando Gunicorn con CHDIR..."
# Usamos --chdir para asegurarnos de que Python busque el módulo 
# 'FeriaVirtual' desde el directorio raíz (que es donde está la carpeta 'FeriaVirtual').
gunicorn --chdir . FeriaVirtual.wsgi:application