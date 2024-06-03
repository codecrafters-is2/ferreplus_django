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
