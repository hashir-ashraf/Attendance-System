from django import template

register = template.Library()

@register.filter
def toInt(s):
    return int(s)


@register.filter
def toStr(i):
    return str(i)