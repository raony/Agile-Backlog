from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    vision_statement = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('project_plan', [self.slug])
    
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
    number = models.PositiveSmallIntegerField(unique=True)
    deadline = models.DateTimeField(null=True, blank=True)
    velocity = models.PositiveIntegerField(null=True, blank=True)
    
    project = models.ForeignKey(Project, related_name='sprints')
    
    def __unicode__(self):
        return 'Sprint %d'%self.number
    
    def has_place(self, item):
        current = self.items.all().aggregate(total = models.Sum('complexity'))['total'] or 0
        return (current + item.complexity) <= self.velocity
    
    class Meta:
        ordering = ['number',]

class Item(models.Model):
    priority = models.PositiveIntegerField(unique=True, null=True)
    summary = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    complexity = models.PositiveIntegerField(default=2)
    
    project = models.ForeignKey(Project, related_name='items', null=True)
    sprint = models.ForeignKey(Sprint, related_name='items', null=True, blank=True)

    def __unicode__(self):
        return self.summary
    
    def previous(self):
        if Item.objects.filter(priority=self.priority-1):
            return Item.objects.get(priority=self.priority-1)
    
    def next(self):
        if Item.objects.filter(priority=self.priority+1):
            return Item.objects.get(priority=self.priority+1)
    
    def up(self):
        prev = self.previous()
        priority = self.priority
        self.priority = prev.priority
        prev.priority = None
        prev.save()
        self.save()
        prev.priority = priority
        prev.save()
    
    @models.permalink
    def get_absolute_url(self):
        return ('item_view', [str(self.id)])
    
    class Meta:
        ordering = ['priority',]
