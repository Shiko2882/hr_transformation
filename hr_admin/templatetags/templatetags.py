from django import template
from hr_admin.models import *

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
@register.filter
def get_field(form, field_name):
    return form[field_name]
register = template.Library()

@register.filter(name='get_answer')
def get_answer(answers, question):
    return answers.filter(question=question).first()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key, None)