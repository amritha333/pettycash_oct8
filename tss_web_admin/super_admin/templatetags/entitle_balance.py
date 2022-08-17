from ast import arg
from django import template

register = template.Library()

from super_admin.models import *

@register.filter(name='leave_taken_method')
def leave_taken_method(value,args):
    result = int(value) - int(args)
    return result