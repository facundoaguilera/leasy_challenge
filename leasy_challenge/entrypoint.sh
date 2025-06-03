#!/bin/bash

echo "Esperando a que la base de datos esté disponible..."
sleep 5

echo "Aplicando migraciones..."
python manage.py migrate

echo "Creando superusuario si no existe..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin123")
    print("Superusuario creado.")
else:
    print("El superusuario ya existe.")
EOF

echo "Creando usuarios de prueba..."
python manage.py create_test_users

echo "Inicialización completa. Ejecutando comando..."
exec "$@"
