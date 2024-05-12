from django.urls import path
from .views import BranchListView, BranchCreateView, BranchUpdateView, BranchDeleteView

urlpatterns = [
    path('branches/', BranchListView.as_view(), name='show_branches'),
    path('branches/add/', BranchCreateView.as_view(), name='register_new_branch'),
    path('branches/edit/<int:pk>/', BranchUpdateView.as_view(), name='edit_branch'),
    path('branches/delete/<int:pk>/', BranchDeleteView.as_view(), name='delete_branch'),
]
