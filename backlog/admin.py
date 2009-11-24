from django.contrib import admin
from models import *

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
#    actions = ['plan',]
    
    
    def plan(self, request, queryset):
        for obj in queryset:
            obj.plan()
            
        if queryset.count() == 1:
            message_bit = "1 project was planned."
        else:
            message_bit = "%s projects were planned." % queryset.count()
        self.message_user(request, message_bit)

class ItemAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'complexity', 'description_trunc', 'sprint', 'project', ]
    list_editable = ['complexity',]

admin.site.register(Item, ItemAdmin)
admin.site.register(Sprint)
admin.site.register(Project, ProjectAdmin)
