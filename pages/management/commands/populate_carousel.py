from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from pages.models import HomeCarouselBanner


class Command(BaseCommand):
    help = "Crea los banners en la base de datos con las imagenes preguardadas en el repositorio."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        banners = [
            {
                "title": "Todo lo que necesitás está acá",
                "description": "Tenemos todo en herramientas nuevas y usadas",
                "img_path": "static/img/carousel/ferreplus_1.jpg",
                "title_position": "left"
            },
            {
                "title": "¡Visitá nuestra tienda!",
                "description": "Llevate tu producto de intercambio y aprovechá las mejores ofertas en insumos de ferretería",
                "img_path": "static/img/carousel/ferreplus_2.jpg",
                "title_position": "left"
            },
            {
                "title": "Sector jardinería",
                "description": "Estamos inaugurando la nueva sección Jardinería, no te la pierdas!",
                "img_path": "static/img/carousel/ferreplus_3.jpg",
                "title_position": "left"
            }
        ]
        
        try:
            for banner in banners:
                nuevo_banner = HomeCarouselBanner.objects.create(
                    title=banner.get("title"),
                    description=banner.get("description"),
                    title_position=banner.get("title_position")
                )

                file_name = banner.get("img_path")
                img_file = File(open(file_name, 'rb'))
                nuevo_banner.image_widescreen.save(
                    file_name.lstrip("static/img/carousel/"),
                    img_file
                )

                nuevo_banner.save()

        except Exception as e:
            raise CommandError(f"Hubo un error al crear los banners: {e}")
        