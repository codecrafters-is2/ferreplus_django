from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from branches.models import Branch

@receiver(post_save, sender=Branch)
def update_posts_state(sender, instance, **kwargs):
    # Verifica si la sucursal se ha desactivado
    if not instance.is_active:
        # Obtiene todos los posts asociados a la sucursal desactivada
        posts = Post.objects.filter(original_branch_id=instance.id)
        # Actualiza el estado de los posts a "paused"
        posts.update(status=Post.POST_STATUS_PAUSED, branch=None)

@receiver(post_save, sender=Post)
def cancel_barter(sender, instance, created, **kwargs):
    if not instance.status == 'available':
        barter = instance.barter
        if not barter.posts.filter(status='available').exists():
            barter.state = 'cancelado'
            barter.save()
