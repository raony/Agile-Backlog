from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import truncate_words

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    vision_statement = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return 'http://localhost:8000%s'%reverse('project_plan', kwargs={'slug': self.slug})
    
    def plan(self, base_velocity, base_date, timedelta, max_number=None):
        if self.sprints.count():
            raise Project.AlreadyPlannedException
        
        if base_velocity < self.items.all().aggregate(max=models.Max('complexity'))['max']:
            raise Project.SmallVelocityException
        
        current_sprint = None
        for item in self.items.all():
            if not current_sprint:
                current_sprint = Sprint.objects.create(number=1, 
                                                       deadline=base_date + timedelta, 
                                                       velocity=base_velocity,
                                                       project=self)
            
            if not current_sprint.has_place(item):
                if max_number and (current_sprint.number == max_number):
                    break
                current_sprint = Sprint.objects.create(number=current_sprint.number + 1, 
                                                       deadline=current_sprint.deadline + timedelta,
                                                       velocity=base_velocity,
                                                       project=self)
            
            item.sprint = current_sprint
            item.save()
    
    def drop_plan(self):
        self.items.all().update(sprint=None)
        self.sprints.all().delete()
    
    class AlreadyPlannedException(Exception):
        pass

    class SmallVelocityException(Exception):
        pass
    
    
class Sprint(models.Model):
    goal = models.TextField(null=True, blank=True)
    number = models.PositiveSmallIntegerField()
    deadline = models.DateTimeField(null=True, blank=True)
    velocity = models.PositiveIntegerField(default=2, blank=True)
    
    project = models.ForeignKey(Project, related_name='sprints')
    
    def __unicode__(self):
        return 'Sprint %d'%self.number
    
    def load(self):
        return self.items.all().aggregate(total = models.Sum('complexity'))['total'] or 0
    
    def has_place(self, item):
        current = self.items.all().aggregate(total = models.Sum('complexity'))['total'] or 0
        return (current + item.complexity) <= self.velocity
    
    def get_absolute_url(self):
        return 'http://localhost:8000%s'%reverse('sprint_view', kwargs={'id': self.id})
    
    def resize(self, number=False):
        current = self.items.all().aggregate(total = models.Sum('complexity'))['total'] or 0
        try:
            next_sprint = Sprint.objects.get(project=self.project, number=self.number+1)
        except Sprint.DoesNotExist:
            next_sprint = None
        
        resized = False
        while current > self.velocity:
            resized = True
            last = self.items.order_by('-priority').all()[0]
            
            nsp_items = list(Item.objects.filter(sprint=next_sprint))
            Item.objects.filter(sprint=next_sprint).update(priority=None)
            nsp_items = [last] + nsp_items
            for i, item in enumerate(nsp_items):
                item.priority = i+1
                item.sprint = next_sprint
                item.save()
            current = self.items.all().aggregate(total = models.Sum('complexity'))['total'] or 0
        
        if number:
            spread = [self.number]
            out = self.number + 1
        else:
            spread = [self.id]
            out = -1
            
        if resized:
            if next_sprint:
                return spread + next_sprint.resize(number)
            else:
                return spread + [out]
        else:
            return spread
#        else:            
#            return []
    
    class Meta:
        ordering = ['number',]
        unique_together = (('number', 'project'),)

class Item(models.Model):
    priority = models.PositiveIntegerField(null=True, blank=True)
    summary = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    complexity = models.PositiveIntegerField(default=2)
    
    project = models.ForeignKey(Project, related_name='items', null=True)
    sprint = models.ForeignKey(Sprint, related_name='items', null=True, blank=True)

    def __unicode__(self):
        return self.summary

    def description_trunc(self):
        return truncate_words(self.description, 18)
    
    def previous(self):
        if Item.objects.filter(priority=self.priority-1):
            return Item.objects.get(priority=self.priority-1)
    
    def next(self):
        if Item.objects.filter(priority=self.priority+1):
            return Item.objects.get(priority=self.priority+1)
    
    def get_absolute_url(self):
        return 'http://localhost:8000%s'%reverse('item_view', kwargs={'id': self.id})
    
    class Meta:
        ordering = ['priority',]
        unique_together = (('priority', 'sprint'),)
