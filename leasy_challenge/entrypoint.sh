#!/bin/bash

echo "Esperando a que la base de datos esté disponible..."
sleep 5

echo "Aplicando migraciones..."
python manage.py migrate

echo "Creando superusuario si no existe..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
User = get_user_model()
if not User.objects.filter(email="admin@leasy.test").exists():
    user = User.objects.create_user(
        email="admin@leasy.test",
        password="admin123",
        first_name="admin",
        is_staff=True,
        is_superuser=True
    )

    roles = ['ventas', 'operaciones', 'cobranzas']
    for role in roles:
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)  # correcto
    print("Superusuario creado.")
else:
    print("El superusuario ya existe.")
EOF

echo "Creando usuarios de prueba..."
python manage.py create_test_users

echo "Inicialización completa. Ejecutando comando..."
exec "$@"
