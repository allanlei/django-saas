from django.conf.urls.defaults import patterns, include, url

import views


item_patterns = patterns('',
#    url(r'^$', views.DetailView.as_view(), name='detail'),
#    url(r'^update/$', views.UpdateView.as_view(), name='update'),
#    url(r'^delete/$', views.DeleteView.as_view(), name='delete'),
)

urlpatterns = patterns('',
    url(r'^$', views.ListView.as_view(), name='list'),
    url(r'^create/$', views.CreateView.as_view(), name='create'),    
#    url(r'^(?P<pk>\d+)/', include(item_patterns)),
)
