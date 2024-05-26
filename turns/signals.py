from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment

@receiver(post_save, sender=Appointment)
def update_barter_state(sender, instance, created, **kwargs):
    if created:
        # Cambiar el estado del trueque a 'aceptado'
        instance.barter.state = 'accepted'
        instance.barter.save()

        # Cambiar el estado de las publicaciones asociadas a 'reservado'
        for post in instance.barter.posts.all():
            post.status = 'reserved'
            post.save()
