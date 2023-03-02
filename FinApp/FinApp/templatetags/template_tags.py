from django import template
from django.forms import model_to_dict

register = template.Library()

@register.filter(name='get')
def get(d, key):
    return dict(d)[key]

@register.filter(name='model_to_dict')
def _model_to_dict(obj):
    return model_to_dict(obj)