#!/bin/sh

# Cargar variables de entorno manualmente
export $(cat .env | grep -v '^#' | xargs)

# Ejecutar comando
/usr/local/bin/python3 manage.py generate_invoices
