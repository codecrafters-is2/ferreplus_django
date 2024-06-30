from django import template

register = template.Library()

@register.inclusion_tag("ui_components/go_back_button.html")
def show_go_back_button(to_url: str) -> dict:
    return {"to": to_url}
