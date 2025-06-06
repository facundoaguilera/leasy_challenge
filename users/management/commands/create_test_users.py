from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from users.models import CustomUser

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        roles = ['ventas', 'operaciones', 'cobranzas']
        
        for role in roles:
            group, _ = Group.objects.get_or_create(name=role)
            email = f'{role}_user@leasy.test'
            if not CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.create_user(
                    email=email,
                    password='leasy1234',
                    first_name=role.capitalize()
                )
                user.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f'Usuario {email} creado y asignado a {role}'))

        self.stdout.write(self.style.SUCCESS('Usuarios de prueba creados.'))
