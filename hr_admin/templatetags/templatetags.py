from django import template
from hr_admin.models import *
from itertools import groupby as it_groupby
from itertools import groupby


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



@register.filter
def groupby_question_category(value):
    keyfunc = lambda x: x.question.category
    return groupby(sorted(value, key=keyfunc), key=keyfunc)
