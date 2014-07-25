from django.conf.urls import patterns, url

from ask import views

urlpatterns = patterns('',
    url(r'^login/$', 'loginsys.views.login'),
    url(r'^logout/$', 'loginsys.views.logout'),
    url(r'^register/$', 'loginsys.views.register'),
	url(r'^profile/$', 'loginsys.views.profile'),
    
)
