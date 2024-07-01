from django.urls import path
from .views import (
    BranchListView,
    BranchCreateView,
    BranchUpdateView,
    BranchDeleteView,
    AdminPanelView,
    EmployeeSignupView,
    EmployeeSuccessView,
    update_company_email,
    update_company_email_success
    
)

urlpatterns = [
    path("", AdminPanelView.as_view(), name="adminpanel"),
    path("branches/", BranchListView.as_view(), name="show_branches"),
    path("branches/add/", BranchCreateView.as_view(), name="register_new_branch"),
    path("branches/edit/<int:pk>/", BranchUpdateView.as_view(), name="edit_branch"),
    path("branches/delete/<int:pk>/", BranchDeleteView.as_view(), name="delete_branch"),
    path("employee_signup/", EmployeeSignupView.as_view(), name="employee_signup"),
    path(
        "success/<int:employee_id>/",
        EmployeeSuccessView.as_view(),
        name="employee_success",
    ),
    path('update-company-email/', update_company_email, name='update_company_email'),
    path('update-company-email/success/', update_company_email_success, name='update_company_email_success')
]
