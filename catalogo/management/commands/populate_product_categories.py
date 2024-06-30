# Django
from django.core.management.base import BaseCommand, CommandError
# Local
from catalogo.constants import PRODUCT_BASE_CATEGORIES
from catalogo.models import ProductCategory
from catalogo.services import get_category_by_name


class Command(BaseCommand):
    help = "Crea y persiste las categorías de base para el Catálogo"

    def add_arguments(self, parser):
        parser.add_argument(
            "--new",
            help="Añade una nueva categoría en lugar de generar las categorías base",
        )

    def handle(self, *args, **options):
        new_category = options.get("new")
        try:
            if new_category:
                category = ProductCategory.objects.create(name=new_category)
                category.save()
            else:
                for base_category in PRODUCT_BASE_CATEGORIES:
                    if not get_category_by_name(base_category):
                        category = ProductCategory.objects.create(
                            name=base_category
                        )
                        category.save()
                        
        except Exception as e:
            raise CommandError(f"Hubo un error al crear las categorías: {e}")
        
        self.stdout.write(self.style.SUCCESS("Categorías creadas exitosamente."))