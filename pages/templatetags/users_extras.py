from django import template
from accounts.models import CustomUser

register = template.Library()

@register.filter(name="belongs_to_group")
def belongs_to_group(user: CustomUser, group_name: str) -> bool:
    return user.groups.filter(name=group_name).exists()

@register.filter(name="group_layout")
def group_layout(user: CustomUser) -> str:
    if user.groups.filter(name="admi").exists():
        return "_base_admin.html"
    if user.groups.filter(name="client").exists():
        return "_base.html"
    if user.groups.filter(name="employee").exists():
        return "_base.html"

@register.filter(name="user_post_search_url")
def user_post_search_url(user: CustomUser) -> str:
    if user.groups.filter(name="admi").exists():
        return "home"
    if user.groups.filter(name="client").exists():
        return 'post_search_results'
    if user.groups.filter(name="employee").exists():
        return 'post_search_employee'
