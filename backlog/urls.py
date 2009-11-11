from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    url(r'^item/(?P<id>\d+)/up/$', 'backlog.views.up', name='item_up'),
    url(r'^item/(?P<id>\d+)/$', 'backlog.views.item', name='item_view'),
    url(r'^item/sort/$', 'backlog.views.sort', name='item_sort'),
    
    url(r'^project/(?P<slug>[\w|\-|\_]+)/plan/$', 'backlog.views.project_plan', name='project_plan'),
    
    url(r'^list_view/$', 'backlog.views.list_view', name='list_view'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
