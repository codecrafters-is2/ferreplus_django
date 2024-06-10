from django.db.models import QuerySet
from posts.models import Post

def get_active_posts() -> QuerySet:
    return Post.objects.filter(status="available")
