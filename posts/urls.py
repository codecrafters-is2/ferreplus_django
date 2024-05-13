from django.urls import path
from django.contrib.auth.decorators import login_required #Para chequear el inicio de sesion
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, MyPostListView


urlpatterns = [
    path("", login_required(PostListView.as_view()), name="post_list"),
    path("my_posts/", login_required(MyPostListView.as_view()), name="my_post_list"),
    path("post/<int:pk>/", login_required(PostDetailView.as_view()), name="post_detail"),
    path("post/new/", login_required(PostCreateView.as_view()), name="post_new"), 
    path("post/<int:pk>/edit/", login_required(PostUpdateView.as_view()), name="post_edit"),
    path("post/<int:pk>/delete/", login_required(PostDeleteView.as_view()), name="post_delete"), 
]
