from celery import shared_task
from .models import Post

@shared_task
def check_all_posts_package_expiry():
    posts = Post.objects.all()
    for post in posts:
        post.check_package_expiry()
