from django import template
from fiber.models import ContentItem

register = template.Library()

@register.simple_tag()
def cms_content(name):
    content = ContentItem.objects.get(name=name)
    return content.content_html