"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.db import IntegrityError
from models import *
from django.core import serializers
from django.template.loader import get_template
from django.template.context import Context
import json

from datetime import timedelta, datetime

class ItemTest(TestCase):
    def setUp(self):
        self.i1 = Item.objects.create(summary='item1', priority=3)
        self.i2 = Item.objects.create(summary='item2', priority=1)
        self.i3 = Item.objects.create(summary='item3', priority=2)
        
    def test_order(self):
        """
        The backlog items should be ordened by priority.
        """
        self.failUnlessEqual(self.i2, Item.objects.all()[0])
        self.failUnlessEqual(self.i3, Item.objects.all()[1])
        self.failUnlessEqual(self.i1, Item.objects.all()[2])
        
        
    def test_priority_uniqueness(self):
        """
        No two backlog items should have the same priority.
        """
        project = Project.objects.create(name='proj1', slug='proj1')
        sprint = Sprint.objects.create(number=1, project=project)
        
        i4 = Item.objects.create(summary='item4', priority=4, sprint=sprint)
        try:            
            i5 = Item.objects.create(summary='item5', priority=4, sprint=sprint)
            self.fail('an exception should be raised.')
        except IntegrityError:
            pass
    
    def test_item_url(self):
        """
        A http get to /item/id/ should return its properties as json.
        """
        response = self.client.get(self.i1.get_absolute_url())
        self.failUnlessEqual(200, response.status_code)
        self.failUnlessEqual(serializers.serialize('json', [self.i1,]),response.content)
    
    def test_item_view(self):
        """
        A http get to /item/id/view should return an html of the item.
        """
        response = self.client.get('/backlog/item/%d/view/'%self.i1.id)
        self.failUnlessEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'item.html')
        self.failUnlessEqual(self.i1, response.context['item'])
        

class SprintTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name='proj1', slug='proj1')
        self.i1 = Item.objects.create(summary='item1', priority=3, project=self.project)
        self.i2 = Item.objects.create(summary='item2', priority=1, project=self.project)
        self.i3 = Item.objects.create(summary='item3', priority=2, project=self.project)
        
    def test_http_set(self):
        """
        A http POST to /sprint/<id>/sort/ with item ids in data should 
        set the sprint backlog.
        """
        target = Sprint.objects.create(project=self.project, number=1, velocity=6)
        response = self.client.post('/backlog/sprint/%d/'%target.id, {'item[]': [self.i3.id,
                                                                       self.i2.id,
                                                                       self.i1.id]})
        self.failUnlessEqual(200, response.status_code)
        self.failUnlessEqual(self.i3, target.items.all()[0])
        self.failUnlessEqual(self.i2, target.items.all()[1])
        self.failUnlessEqual(self.i1, target.items.all()[2])
    
    def test_http_set_overflow(self):
        """
        When a http POST to /sprint/<id>/sort/ with item that is greater than
        sprint capacity, the sprints should be resized and the spread returned.
        """
        target = Sprint.objects.create(project=self.project, number=1)
        target2 = Sprint.objects.create(project=self.project, number=2)
        response = self.client.post('/backlog/sprint/%d/'%target.id, {'item[]': [self.i3.id,
                                                                       self.i2.id,
                                                                       self.i1.id]})
        self.failUnlessEqual('[1, 2, -1]', response.content)
        self.failUnlessEqual(200, response.status_code)
        self.failUnlessEqual(1, target.items.count())
        self.failUnlessEqual(self.i3, target.items.all()[0])
        self.failUnlessEqual(1, target2.items.count())
        self.failUnlessEqual(self.i2, target2.items.all()[0])
    
    def test_sprint_url(self):
        """
        A http get to /sprint/<id>/ should return its properties as json.
        """
        target = Sprint.objects.create(project=self.project, number=1)
        Item.objects.create(summary='item 1', priority=1, sprint=target)
        response = self.client.get(target.get_absolute_url())
        self.failUnlessEqual(200, response.status_code)
        self.failUnlessEqual(serializers.serialize('json', [target] + list(target.items.all())),response.content)
    
    def test_sprint_view(self):
        """
        A http get to /sprint/id/view should return an html of the sprint.
        """
        target = Sprint.objects.create(project=self.project, number=1)
        response = self.client.get('/backlog/sprint/%d/view/'%target.id)
        self.failUnlessEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'sprint.html')
        self.failUnlessEqual(target, response.context['sprint'])
        
class ProjectTest(TestCase):
    def test_project_plan_view(self):
        """
        A project plan should be accessible at /backlog/project-name-slug/plan
        """
        target = Project.objects.create(name='test project', slug='test_project')
        items = []
        for i in range(10):
            items.append(Item.objects.create(project=target, summary='item%d'%i, complexity=i%6 or 1))
        
        delta =  timedelta(30)
        now = datetime.now()
        
        target.plan(7, now, delta, 3)
        
#        self.failUnlessEqual('/backlog/project/%s/plan/'%target.slug, target.get_absolute_url())
        
        response = self.client.get(target.get_absolute_url())
        self.failUnlessEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'plan.html')
        self.failUnlessEqual([1,2,3,4], response.context['sprints'])
    
    def test_project_sprint_view(self):
        """
        One should be able to retrieve a sprint view through /project/<slug>/sprint/<number> url.
        """
        target = Project.objects.create(name='test project', slug='test_project')
        sp1 = Sprint.objects.create(project=target, number=1)
        response = self.client.get('/backlog/project/test_project/sprint/%d/'%sp1.number)
        self.failUnlessEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'sprint.html')
        self.failUnlessEqual(sp1, response.context['sprint'])
    
    def test_project_view(self):
        """
        A http get to /project/<id>/ should return its properties as json.
        """
        target = Project.objects.create(name='test project', slug='test_project')
        for i in range(5):
            Sprint.objects.create(project=target, deadline=datetime.now(), number=i)
        
        response = self.client.get('/backlog/project/%d/'%target.id)
        self.failUnlessEqual(200, response.status_code)
        self.failUnlessEqual(serializers.serialize('json', [target] + list(target.sprints.all())),response.content)
    
    def test_plan(self):
        """
        Each sprint should be created whenever there is still backlog items left until
        a maximum. It should consider a velocity parameter and a duration parameter.
        """
        target = Project.objects.create(name='test project', slug='test-project')
        items = []
        for i in range(10):
            items.append(Item.objects.create(project=target, summary='item%d'%i, complexity=i%6 or 1))
        
        delta =  timedelta(30)
        now = datetime.now()
        
        target.plan(7, now, delta, 3)
        sprints = target.sprints.all()
        
        self.failUnlessEqual(1, sprints[0].number)
        self.failUnlessEqual(now+delta, sprints[0].deadline)
        self.failUnlessEqual(4, sprints[0].items.count())
        self.failUnless(all([i in sprints[0].items.all() for i in items[:4]]))
        
        self.failUnlessEqual(2, sprints[1].number)
        self.failUnlessEqual(now+delta*2, sprints[1].deadline)
        self.failUnlessEqual(1, sprints[1].items.count())
        self.failUnless(all([i in sprints[1].items.all() for i in items[4:5]]))
        
        self.failUnlessEqual(3, sprints[2].number)
        self.failUnlessEqual(now+delta*3, sprints[2].deadline)
        self.failUnlessEqual(3, sprints[2].items.count())
        self.failUnless(all([i in sprints[2].items.all() for i in items[5:8]]))
        
        try:
            target.plan(7, now, delta, 3)
            self.fail('should raise an AlreadyPlannedException.')
        except Project.AlreadyPlannedException:
            pass
        
        target.drop_plan()
        
        self.failIf(any([i.sprint for i in target.items.all()]))
        self.failIf(target.sprints.all())
        
        Item.objects.create(project=target, summary='large item', complexity=50)
        
        try:
            target.plan(7, now, delta, 3)
            self.fail('should raise an SmallVelocityException.')
        except Project.SmallVelocityException:
            pass
        
        
        
        
    
