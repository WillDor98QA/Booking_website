from django import template
from ..models import *

register = template.Library()


@register.filter
def get_service_id():
    
    return 0