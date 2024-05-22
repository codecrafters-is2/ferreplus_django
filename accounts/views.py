from allauth.account.views import SignupView
from .forms import EmployeeUserCreationForm


class EmployeeSignupView(SignupView):
    template_name = "account/employee_signup.html"
    form_class = EmployeeUserCreationForm
