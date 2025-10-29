from django import template

register = template.Library()

@register.filter
def abs(value):
    """Return absolute value."""
    try:
        return abs(value)
    except Exception:
        return value
