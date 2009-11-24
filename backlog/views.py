# Create your views here.
from django.utils import simplejson
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
        
        for i, id in enumerate(id_list):
            item = Item.objects.get(id=id)
            item.priority = i+1
            item.sprint = t_sprint
            item.save()
        return HttpResponse(simplejson.dumps(t_sprint.resize()))
    
    return HttpResponse(serializers.serialize('json', [t_sprint] + list(t_sprint.items.all())))

def sprint_html_view(request, id):
    return render_to_response('sprint.html', {'sprint': Sprint.objects.get(id=id),
                                              'items_json': simplejson.dumps([item.id for item in Item.objects.filter(sprint=id)])},
                              context_instance=RequestContext(request))

def project_sprint(request, slug, number):
    try:
        sprint = Sprint.objects.get(project__slug=slug, number=number)
        template = 'sprint.html'
    except Sprint.DoesNotExist:
        sprint = None
        template = 'out.html'
    items = Item.objects.filter(project__slug=slug, sprint=sprint)
    
    if request.method == 'POST':
        id_list = [int(x) for x in request.POST.getlist('item[]')]
        items.update(priority=None, sprint=None)
        
        for i, id in enumerate(id_list):
            item = Item.objects.get(id=id)
            item.priority = i+1
            item.sprint = sprint
            item.save()
        
        if sprint:
            return HttpResponse(simplejson.dumps(sprint.resize(True)))
        else:
            return HttpResponse(simplejson.dumps([]))
    
    return render_to_response(template, {'sprint': sprint,
                                         'sprint_num': number,
                                         'items': items,
                                         'items_json': simplejson.dumps([item.id for item in items])},
                              context_instance=RequestContext(request))

def project_plan(request, slug):
    project = Project.objects.get(slug=slug)
    sprints = list(project.sprints.all().values_list('number', flat=True))
    sprints = sprints + [sprints[-1]+1]
    return render_to_response('plan.html', { 'project': project, 
                                             'sprints': sprints,
                                             'sprints_json': simplejson.dumps(sprints),
                                           }, 
                              context_instance=RequestContext(request))

def project_view(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return Http404()
    return HttpResponse(serializers.serialize('json', [project] + list(project.sprints.all())))