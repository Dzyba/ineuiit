from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

@register.filter(name='nbsp')
@stringfilter
def nbsp(value):
    return mark_safe(re.sub(r'\s', '&nbsp;', value))