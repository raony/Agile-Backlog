from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    url(r'^item/(?P<id>\d+)/$', 'backlog.views.item_view', name='item_view'),
    url(r'^item/(?P<id>\d+)/view/$', 'backlog.views.item_html_view', name='item_html_view'),
    
    url(r'^sprint/(?P<id>\d+)/$', 'backlog.views.sprint_view', name='sprint_view'),
    
    url(r'^project/(?P<slug>[\w|\-|\_]+)/plan/$', 'backlog.views.project_plan', name='project_plan'),
    url(r'^project/(?P<id>\d+)/$', 'backlog.views.project_view', name='project_view'),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
