from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=250)
    vision_statement = models.TextField(null=True, blank=True)
    
    
    
class Sprint(models.Model):
    goal = models.TextField(null=True, blank=True)
    number = models.PositiveSmallIntegerField(unique=True)
    deadline = models.DateField(null=True, blank=True)
    velocity = models.PositiveIntegerField(null=True, blank=True)
    
    def __unicode__(self):
        return 'Sprint %d'%self.number
    
    class Meta:
        ordering = ['number',]

class Item(models.Model):
    priority = models.PositiveIntegerField(unique=True, null=True)
    summary = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    complexity = models.PositiveIntegerField(default=2)
    
    project = models.ForeignKey(Project, related_name='items')
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
