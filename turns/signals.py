from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Post

@receiver(post_save, sender=Post)
def cancel_barter(sender, instance, created, **kwargs):
    if not instance.status == 'available':
        barter = instance.barter
        if not barter.posts.filter(status='available').exists():
            barter.state = 'cancelado'
            barter.save()
