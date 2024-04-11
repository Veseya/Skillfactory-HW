from django import template

register = template.Library()



@register.filter()
def censor(value):
    censor_list = ["Победа", "Спешите"]
    for word in censor_list:
        value = value.replace(word[1:], "*" * len(word[1:]))
    return value

