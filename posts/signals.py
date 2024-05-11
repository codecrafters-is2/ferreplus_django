from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Post
from branches.models import Branch

@receiver(post_delete, sender=Branch)
def update_posts_state(sender, instance, **kwargs):
    # Obtiene todos los posts asociados a la sucursal eliminada
    posts = Post.objects.filter(original_branch_id=instance.id)
    # Resto del código para actualizar el estado de los posts
    # Actualiza el estado de los posts a "paused"
    posts.update(status=Post.POST_STATUS_PAUSED)
    