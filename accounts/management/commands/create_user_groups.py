from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from accounts.models import CustomUser

class Command(BaseCommand):
    help = "Crea los grupos que se requieren para asignar a los usuarios"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            Group.objects.get_or_create(name='admi')
            Group.objects.get_or_create(name='client')
            Group.objects.get_or_create(name='employee')

            User = get_user_model()
            User.objects.create_user('admi', 'ferreplusgestion@gmail.com', 'admi')
            usuario = CustomUser.objects.get(username='admi')
            grupo = Group.objects.get(name='admi')
            usuario.groups.add(grupo)

            self.stdout.write(
                self.style.SUCCESS("Grupos creados exitosamente")
            )
        except Exception as e:
            raise CommandError(f"Hubo un error al crear los grupos: {e}")
        