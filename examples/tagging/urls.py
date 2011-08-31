from django.conf.urls.defaults import patterns, include, url

from app.login import CreateView, LoginView, LogoutView

authentication_patterns = patterns('',
    url(r'^create/$', CreateView.as_view(), name='create'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
)

urlpatterns = patterns('',
    url(r'^accounts/', include(authentication_patterns)),
    url(r'^', include('app.urls')),
    
#    url(r'^', include('app.urls', namespace='item')),
#    url(r'^', include('app.urls', namespace='item')),
    
#    url(r'^tenant/', include('app.tenant.urls', namespace='tenant')),    
)
