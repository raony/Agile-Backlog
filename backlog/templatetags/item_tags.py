from django import template

register = template.Library()

@register.inclusion_tag('item.html')
def item_show(item):
    return { 'item': item }    