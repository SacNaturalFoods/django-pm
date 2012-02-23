from django import template
from django.conf import settings

register = template.Library()

@register.filter()
def ipdb(element):
    import ipdb; ipdb.set_trace()
    return element


