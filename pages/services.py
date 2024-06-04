from .models import HomeCarouselBanner


def get_active_banners():
    return HomeCarouselBanner.objects.filter(active=True)
