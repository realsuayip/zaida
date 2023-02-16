from django import template

from asu.models import ProjectVariable

register = template.Library()


@register.simple_tag
def get_variable(name):
    """
    A template tag to get some constant values used in templates:
         {% get_variable "build.BRAND" as brand %}
         The brand is: {{ brand }}
    """
    return ProjectVariable.objects.get_value(name=name)
