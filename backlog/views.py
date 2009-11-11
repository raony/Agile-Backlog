# Create your views here.
import json
from django.http import HttpResponse, Http404
from django.core import serializers
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *


def item_view(request, id):
    return HttpResponse(serializers.serialize('json', Item.objects.filter(id=id)))

def item_html_view(request, id):
    return render_to_response('item.html', {'item': Item.objects.get(id=id),},
                              context_instance=RequestContext(request))

def sprint_view(request, id):
    try:
        t_sprint = Sprint.objects.get(id=id)
    except Sprint.DoesNotExist:
        return Http404()
    
    if request.method == 'POST':
        id_list = [int(x) for x in request.POST.getlist('item[]')]
        t_sprint.items.all().update(priority=None, sprint=None)
        print t_sprint.items.all()
        for i, id in enumerate(id_list):
            item = Item.objects.get(id=id)
            item.priority = i+1
            item.sprint = t_sprint
            item.save()
        return HttpResponse(json.dumps(t_sprint.resize()))
    
    return HttpResponse(serializers.serialize('json', [t_sprint] + list(t_sprint.items.all())))

def project_plan(request, slug):
    project = Project.objects.get(slug=slug)
    return render_to_response('item_list.html', { 'project_id': project.id, 
                                                 'sprints': project.sprints.all() }, 
                              context_instance=RequestContext(request))

def project_view(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return Http404()
    return HttpResponse(serializers.serialize('json', [project] + list(project.sprints.all())))