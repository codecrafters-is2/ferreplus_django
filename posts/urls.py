from django.urls import path
from django.contrib.auth.decorators import login_required #Para chequear el inicio de sesion
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, MyPostListView,MyPostDetailView, DeleteQuestionView, DeleteAnswerView


urlpatterns = [
    path("",PostListView.as_view(), name="post_list"),
    path("my_posts/",MyPostListView.as_view(), name="my_post_list"),
    path("post/<int:pk>/",PostDetailView.as_view(), name="post_detail"),
    path("my_post/<int:pk>/",MyPostDetailView.as_view(), name="my_post_detail"),
    path("post/new/",PostCreateView.as_view(), name="post_new"), 
    path("post/<int:pk>/edit/",PostUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/",PostDeleteView.as_view(), name="post_delete"),
    path('delete_question/<int:question_id>/', DeleteQuestionView.as_view(), name='delete_question'),
    path('delete_answer/<int:question_id>/', DeleteAnswerView.as_view(), name='delete_answer'),
]
