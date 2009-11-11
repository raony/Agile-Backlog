from django.contrib import admin
from models import *

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Item)
admin.site.register(Sprint)
admin.site.register(Project, ProjectAdmin)