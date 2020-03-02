from django import template

register = template.Library()

@register.filter(name='strorlist')
def strorlist(value):
    if isinstance(value, str) == True:
        return "str"
    return "list"

@register.filter('spliter')
def spliter(value):
    value = value.split(" | ") if " | " in value else value
    return value

@register.filter(name='indexer')
def indexer(value, arg):
    a,b = arg.split(",")
    return value[int(a):int(b)]

@register.filter(name="comotline")
def comotline(value):
    if "\\n" in value:
        return value.replace("\\n", " ")
    return value
