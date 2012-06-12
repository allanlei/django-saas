from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required

import views


item_patterns = patterns('',
#    url(r'^$', views.DetailView.as_view(), name='detail'),
#    url(r'^update/$', views.UpdateView.as_view(), name='update'),
#    url(r'^delete/$', views.DeleteView.as_view(), name='delete'),
)

urlpatterns = patterns('',
    url(r'^$', login_required(views.HomeView.as_view()), name='home'),
    url(r'^pizza/create/$', login_required(views.PizzaCreateView.as_view()), name='create_pizza'),
    url(r'^topping/create/$', login_required(views.ToppingCreateView.as_view()), name='create_topping'),
#    url(r'^create/$', views.CreateView.as_view(), name='create'),
#    url(r'^(?P<pk>\d+)/', include(item_patterns)),
)
