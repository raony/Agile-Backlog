# Create your views here.
from django.http import HttpResponse, Http404
from django.core import serializers
from models import *

def up(request, id):
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        return Http404()
    item.up()
    return HttpResponse('ok')

def item(request, id):
    return HttpResponse(serializers.serialize('json', Item.objects.filter(id=id)))