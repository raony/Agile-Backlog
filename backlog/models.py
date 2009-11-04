from django.db import models

# Create your models here.

class Item(models.Model):
    priority = models.PositiveIntegerField(unique=True, null=True)
    summary = models.CharField(max_length=250)

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
