from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    url(r'^', include('app.urls', namespace='item')),
    
    url(r'^tenant/', include('app.tenant.urls', namespace='tenant')),    
)
