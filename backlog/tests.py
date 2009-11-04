"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.db import IntegrityError
from models import *
from django.core import serializers


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
    
    def test_priority_up(self):
        """
        A http POST to /item/id/up should increase its priority.
        """
        response = self.client.post('/backlog/item/%d/up/'%self.i1.id)
        self.failUnlessEqual(200, response.status_code)
        
        self.failUnlessEqual(self.i2, Item.objects.all()[0])
        self.failUnlessEqual(self.i1, Item.objects.all()[1])
        self.failUnlessEqual(self.i3, Item.objects.all()[2])
    
    def test_item_url(self):
        """
        A http get to /item/id/ should return its properties as json.
        """
        response = self.client.get(self.i1.get_absolute_url())
        self.failUnlessEqual(200, response.status_code)
        self.failUnlessEqual(serializers.serialize('json', [self.i1,]),response.content)
    
    
