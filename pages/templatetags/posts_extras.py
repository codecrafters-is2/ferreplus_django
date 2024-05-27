from django import template
from branches.models import Branch
from posts.constants import Categories

register = template.Library()

"""
    Custom tags para integrar como componentes
"""


@register.inclusion_tag("ui_components/categories_selector.html")
def show_categories_selector() -> dict:
    categories_list = []
    for category in Categories:
        categories_list.append({
            "name": category.name.lower().replace("_"," "),
            "db_name": category.value
        })

    return { "categories": categories_list }


@register.inclusion_tag("ui_components/branches_selector.html")
def show_branches_selector() -> dict:
    branches_list = list()
    branches_list.append({
        "name": "todas",
        "id": ""
    })
    branches = Branch.objects.filter(is_active=True)
    for branch in branches:
        branches_list.append({"name": branch.__str__(), "id": branch.id})

    return {"branches": branches_list}