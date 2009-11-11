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

def sort(request):
    list = [int(x) for x in request.POST.getlist('item[]')]
    Item.objects.filter(id__in=list).update(priority=None)
    for i, id in enumerate(list):
        item = Item.objects.get(id=id)
        item.priority = i+1
        item.save()
    return HttpResponse('')

def list_view(request):
    return render_to_response('item_list.html', { 'items': Item.objects.all() }, 
                              context_instance=RequestContext(request))

def project_plan(request, slug):
    project = Project.objects.get(slug=slug)
    return render_to_response('item_list.html', { 'sprints': project.sprints.all() }, 
                              context_instance=RequestContext(request))