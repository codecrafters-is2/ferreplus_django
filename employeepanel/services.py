# Django
from django.db.models import QuerySet
# Local
from accounts.models import EmployeeUser
from posts.models import Post


def get_employee_post_list(employee: EmployeeUser) -> QuerySet:
    return Post.objects.filter(branch=employee.branch)
