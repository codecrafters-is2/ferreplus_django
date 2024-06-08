from django import template
from pages.models import HomeCarouselBanner
from pages.services import get_active_banners

register = template.Library()

"""
    Custom tags para integrar como componentes
"""


@register.inclusion_tag("ui_components/home_carousel.html")
def show_home_banner() -> dict:
    active_banners = get_active_banners()
    banners = []
    number = 0
    for banner in active_banners:
        banners.append({
            "title": banner.title,
            "image_widescreen": banner.image_widescreen,
            "description": banner.description,
            "number": number
        })
        number += 1

    return {"banners": banners}


@register.inclusion_tag("ui_components/home_site_features.html")
def show_home_site_features() -> dict:
    """ Por ahora es info estática pero me sirve para ordenar el código"""
    features = [
        { "name": "Jardín", "img_source": "img/icons/features/garden.png" },
        { "name": "Herramientas", "img_source": "img/icons/features/tools.png" },
        { "name": "Plomería", "img_source": "img/icons/features/plumbing.png" },
        { "name": "Electricidad", "img_source": "img/icons/features/electricity.png" },
        { "name": "Construcción", "img_source": "img/icons/features/build.png" },
    ]
    return {
        "title": "Conocé nuestra plataforma de trueques",
        "subtitle": "Tenemos un revolucionario sistema de trueques para que puedas intercambiar aquellos artículos que ya no te sirven por otros que estés necesitando",
        "categories": "¡Contamos con productos de todas las categorías!",
        "features": features
    }
