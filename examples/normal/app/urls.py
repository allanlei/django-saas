from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required

import views


urlpatterns = patterns('',
    url(r'^$', login_required(views.HomeView.as_view()), name='home'),
    url(r'^pizza/create/$', login_required(views.PizzaCreateView.as_view()), name='create_pizza'),
    url(r'^topping/create/$', login_required(views.ToppingCreateView.as_view()), name='create_topping'),
)
