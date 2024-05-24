from django import template
from branches.models import Branch
from posts.constants import Categories

register = template.Library()

@register.inclusion_tag("ui_components/categories.html")
def show_categories() -> list[str]:
    categories_list = []
    for category in Categories:
        categories_list.append({ "name": category.name.lower(), "db_name": category.value })

    return { "categories": categories_list }