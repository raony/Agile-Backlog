# Create your views here.
from django.http import HttpResponse, Http404
from django.core import serializers
from django.shortcuts import render_to_response
from django.template import RequestContext
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

def list_view(request):
    return render_to_response('item_list.html', { 'items': Item.objects.all() }, 
                              context_instance=RequestContext(request))