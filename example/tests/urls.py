from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^list/$', views.DetailView.as_view(), name='detail'),
    url(r'^create/$', views.CreateView.as_view(), name='create'),
    url(r'^create/db/$', views.CreateDBView.as_view(), name='create_db'),
    url(r'^delete/db/(?P<pk>.*)/$', views.DeleteDBView.as_view(), name='delete_db'),
)
