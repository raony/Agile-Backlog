# Create your views here.
from django.http import HttpResponse, Http404
from django.core import serializers
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *

def item(request, id):
    return HttpResponse(serializers.serialize('json', Item.objects.filter(id=id)))

def sprint(request, id):
    t_sprint = Sprint.objects.filter(id=id)
    if request.method == 'POST':
        list = [int(x) for x in request.POST.getlist('item[]')]
        if t_sprint:
            t_sprint = t_sprint[0]
        else:
            return Http404()
        
        t_sprint.items.all().update(priority=None, sprint=None)
        
        for i, id in enumerate(list):
            item = Item.objects.get(id=id)
            print '%s = %s - %s'%(unicode(item), unicode(item.priority), unicode(item.sprint))
            item.priority = i+1
            item.sprint = t_sprint
            item.save()
        return HttpResponse('')
    return HttpResponse(serializers.serialize('json', t_sprint))

def list_view(request):
    return render_to_response('item_list.html', { 'items': Item.objects.all() }, 
                              context_instance=RequestContext(request))

def project_plan(request, slug):
    project = Project.objects.get(slug=slug)
    return render_to_response('item_list.html', { 'sprints': project.sprints.all() }, 
                              context_instance=RequestContext(request))