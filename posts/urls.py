from django.urls import path
from django.contrib.auth.decorators import login_required #Para chequear el inicio de sesion
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, MyPostListView


urlpatterns = [
    path("",PostListView.as_view(), name="post_list"),
    path("my_posts/",MyPostListView.as_view(), name="my_post_list"),
    path("post/<int:pk>/",PostDetailView.as_view(), name="post_detail"),
    path("post/new/",PostCreateView.as_view(), name="post_new"), 
    path("post/<int:pk>/edit/",PostUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/",PostDeleteView.as_view(), name="post_delete"), 
]
