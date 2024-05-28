from django.urls import path
from .views import UserDetailWithPostsView


urlpatterns = [
    path("user/<int:user_id>/", UserDetailWithPostsView.as_view(), name="user_detail"),
]
