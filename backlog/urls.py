from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    url(r'^item/(?P<id>\d+)/$', 'backlog.views.item', name='item_view'),
    
    url(r'^sprint/(?P<id>\d+)/$', 'backlog.views.sprint', name='sprint_view'),
    
    url(r'^project/(?P<slug>[\w|\-|\_]+)/plan/$', 'backlog.views.project_plan', name='project_plan'),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
