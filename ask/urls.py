from django.conf.urls import patterns, url

from ask import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^pop/$', views.popindex, name='popindex'),
    url(r'^tags/(?P<id>\d+)/$', views.tags, name='tags'),
    url(r'^(?P<id>\d+)/$', views.ask, name='ask'),
    url(r'^(?P<id>\d+)/page/(?P<page_number>\d+)/$', views.ask, name='ask'),
    url(r'^qplus/$', views.qplus, name='qplus'),
    url(r'^qminus/$', views.qminus, name='qminus'),
    url(r'^correct/$', views.correct, name='correct'),
    url(r'^aplus/$', views.aplus, name='aplus'),
    url(r'^aminus/$', views.aminus, name='aminus'),
    url(r'^addcomment/(?P<id>\d+)/$', views.addcomment),
    url(r'^page/(\d+)/$', views.index),
    url(r'^pop/page/(\d+)/$', views.popindex),
    url(r'^tags/(?P<id>\d+)/page/(?P<page_number>\d+)/$', views.tags, name='tags'),
    url(r'^/$', views.index),
    url(r'^newask/$', views.newask),
    url(r'^search/$', views.search, name="search"),
    url(r'^search/page/(\d+)/$', views.search, name="search"),
)
