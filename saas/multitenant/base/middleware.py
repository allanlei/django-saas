from django.utils.functional import curry

from signals import db_route_read, db_route_write
        

class BaseMultiTenantMiddleware(object):
    signal_function = None
    signals = [db_route_read, db_route_write]
    
    def get_signal_function(self, **kwargs):
        if self.signal_function:
            function = self.signal_function
        else:
            raise ImproperlyConfigured('Provide signal_function or override get_signal_function().')
        return function
    
    def get_dispatch_uid(self, request):
        return request
    
    def get_signals(self):
        if self.signals is not None:
            signals = self.signals
        else:
            raise ImproperlyConfigured('Provide signals')
        return signals
        
    def connect_signals(self, request, weak=False, **kwargs):
        signal_function = self.get_signal_function(request=request)
        for signal in self.get_signals():
            signal.connect(signal_function, weak=weak, dispatch_uid=self.get_dispatch_uid, **kwargs)
    
    def disconnect_signals(self, request, weak=False, **kwargs):
        for signal in self.get_signals():
            signal.disconnect(weak=weak, dispatch_uid=self.get_dispatch_uid(request), **kwargs)
        
    def process_request(self, request):
        self.connect_signals(request)
        return None
        
    def process_response(self, request, response):
        self.disconnect_signals(request)
        return response
    
    
class RequestMultiTenantMixin(self):
    @classmethod
    def get_request(cls, sender, request=None, **kwargs):
        return request
    
    def get_signal_function(self, request=request):
        return curry(self.get_request, request=request)


class RequestAttributeMultTenantMixin(RequestMultiTenantMixin):
    @classmethod
    def get_request(cls, sender, request=None, **kwargs):
        return request and request.GET.get('domain', 'default') or None
    

    
#from saas.multidb.models import Database
#from django.core.exceptions import MiddlewareNotUsed
#class AutoLoadMiddleware(object):
#    def __init__(self):
#        Database.objects.load()
#        raise MiddlewareNotUsed()
