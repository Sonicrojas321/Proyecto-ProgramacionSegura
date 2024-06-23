from django import template
from django.utils import timezone

register = template.Library()

@register.filter(name='is_past_due')
def is_past_due(fecha_cierre):
    return fecha_cierre <= timezone.now()
