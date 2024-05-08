from django.urls import path
from django.contrib.auth.decorators import login_required #Para chequear el inicio de sesion
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView


urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/new/", PostCreateView.as_view(), name="post_new"), 
    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"), 
    #Ejemplo de chequear inicio de sesion: path("post/new/", login_required(PostCreateView.as_view()), name="post_new"),
]
