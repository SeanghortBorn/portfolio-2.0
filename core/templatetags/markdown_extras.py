import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="render_markdown")
def render_markdown(value):
    """Converts Markdown text into safe HTML with fenced code blocks and tables."""
    if not value:
        return ""
    html = markdown.markdown(
        value,
        extensions=["extra", "fenced_code", "nl2br", "sane_list"],
    )
    return mark_safe(html)