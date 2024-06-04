from django.db import models


class HomeCarouselBanner(models.Model):
    title = models.CharField(default='imagen_banner', max_length=100, null=False)
    title_position = models.CharField(default="right", max_length=20)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    image_widescreen = models.ImageField(upload_to='home/banner', null=False)
    # Después podemos linkear con producto de catálogo u otro link
    
    def __str__(self):
        return f"{self.title} - {'active' if self.active else 'disabled'}"