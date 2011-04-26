from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required

import views

urlpatterns = patterns('',
    url(r'^$', views.ListView.as_view(), name='list'),
    url(r'^user/create/$', views.UserCreateView.as_view(), name='user_create'),
    url(r'^testdata/create/$', views.TestDataCreateView.as_view(), name='testdata_create'),
)
