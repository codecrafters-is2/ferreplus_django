from django.urls import path
from .views import PostListView, PostDetailView, DeleteAnswerView, DeleteQuestionView, PostSearchView, PostDeleteView

urlpatterns = [
    path("posts/",PostListView.as_view(), name="post_list_employee"),
    path("posts/search/",PostSearchView.as_view(), name="post_search_employee"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail_employee"),
    path("post/<int:pk>/delete_question/<int:question_id>/", DeleteQuestionView.as_view(), name="delete_question_employee"),
    path("post/<int:pk>/delete_answer/<int:question_id>/", DeleteAnswerView.as_view(), name="delete_answer_employee"),
    path("post/<int:pk>/delete_post_employee",PostDeleteView.as_view(), name="post_delete_employee")
]
