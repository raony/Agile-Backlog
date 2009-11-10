from django import template

register = template.Library()

@register.inclusion_tag('item.html')
def item_show(item):
    return { 'item': item }    

@register.filter
def complexity_size(val):
    return min(15 + int(val * 0.22), 23)

@register.filter
def complexity_height(val):
    return 15 + val/2