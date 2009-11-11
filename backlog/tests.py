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
        i4 = Item.objects.create(summary='item4', priority=4)
        try:            
            i5 = Item.objects.create(summary='item5', priority=4)
            self.fail('an exception should be raised.')
        except IntegrityError:
            pass
    
    def test_priority_up(self):
        """
        item.up() should switch its order with the immediately superior.
        """
        self.i1.up()
        
        self.failUnlessEqual(self.i2, Item.objects.all()[0])
        self.failUnlessEqual(self.i1, Item.objects.all()[1])
        self.failUnlessEqual(self.i3, Item.objects.all()[2])
    
    def test_priority_http_up(self):
        """
        A http POST to /item/id/up should increase its priority.
        """
        response = self.client.post('/backlog/item/%d/up/'%self.i1.id)
        self.failUnlessEqual(200, response.status_code)
        
        self.failUnlessEqual(self.i2, Item.objects.all()[0])
        self.failUnlessEqual(self.i1, Item.objects.all()[1])
        self.failUnlessEqual(self.i3, Item.objects.all()[2])
    
    def test_priority_http_set(self):
        """
        A http POST to /item/sort/ with ids in data should change its priority.
        """
        response = self.client.post('/backlog/item/sort/', {'item[]': [3,2,1]})
        self.failUnlessEqual(self.i3, Item.objects.all()[0])
        self.failUnlessEqual(self.i2, Item.objects.all()[1])
        self.failUnlessEqual(self.i1, Item.objects.all()[2])
    
    def test_item_url(self):
        """
        A http get to /item/id/ should return its properties as json.
        """
        response = self.client.get(self.i1.get_absolute_url())
        self.failUnlessEqual(200, response.status_code)
        self.failUnlessEqual(serializers.serialize('json', [self.i1,]),response.content)

class ListViewTest(TestCase):
#    def test_item_template(self):
#        """
#        There is a template for item that shows its summary and description in separated divs.
#        """
#        template = get_template('item.html')
#        
#        result = template.render(Context({'item' : Item(id=4, summary='item1', description='description1')}))
#        self.failUnlessEqual('<div id="item_4"><div id="summary">item1</div><div id="description">description1</div></div>', 
#                             result)
    
    def test_item_list(self):
        """
        A http GET to /backlog/list_view should load the item_list.html template with all
        the items in the base.
        """
        i1 = Item.objects.create(summary='item1', priority=3)
        i2 = Item.objects.create(summary='item2', priority=1)
        i3 = Item.objects.create(summary='item3', priority=2)
        
        response = self.client.get('/backlog/list_view/')
        self.failUnless('items' in response.context)
        self.failUnlessEqual(3, len(response.context['items']))
        self.failUnless(all([i in response.context['items'] for i in [i1, i2, i3]]))
        self.assertTemplateUsed(response, 'item_list.html')
    
class ProjectTest(TestCase):
    def test_project_view(self):
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
        
        self.failUnlessEqual('/backlog/project/%s/plan/'%target.slug, target.get_absolute_url())
        
        response = self.client.get(target.get_absolute_url())
        self.failUnlessEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'item_list.html')
        self.failUnless(all([sprint in target.sprints.all() for sprint in response.context['sprints']]))
        self.failUnless(all([sprint in response.context['sprints'] for sprint in target.sprints.all()]))
    
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
        
        
        
        
    
