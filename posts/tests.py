from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Post

class PostsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secret"
        )
        cls.post = Post.objects.create(
            title="A good title",
            body="Nice body content",
            author=cls.user,
            category=Post.HERRAMIENTAS,
            status=Post.POST_STATUS_AVAILABLE,
        )
        
    def test_post_model(self):
        print(f"self.post.title:  {self.post.title}")
        self.assertEqual(self.post.title, "A good title")
        self.assertEqual(self.post.body, "Nice body content")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(str(self.post), "A good title")
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")
        self.assertEqual(self.post.category, Post.HERRAMIENTAS)
        self.assertEqual(self.post.status, Post.POST_STATUS_AVAILABLE)