from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Crea los grupos que se requieren para asignar a los usuarios"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            Group.objects.get_or_create(name='admi')
            Group.objects.get_or_create(name='client')
            Group.objects.get_or_create(name='employee')
            self.stdout.write(
                self.style.SUCCESS("Grupos creados exitosamente")
            )
        except Exception as e:
            raise CommandError(f"Hubo un error al crear los grupos: {e}")
        