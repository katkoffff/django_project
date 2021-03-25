from django import template

register = template.Library()

@register.filter(name='censors')
def censors(value):
    profanity=['Бакс', 'Хит', 'Акулы', 'акулы', 'адронный', 'частиц', 'Викинги', 'викинги', 'vikings', 'конунг', 'провидцы']
    b='<BEEP>'
    for p in profanity:
        value = value.replace(p,b)
    return value
