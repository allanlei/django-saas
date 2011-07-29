from django.utils.functional import curry

from signals import db_route_read, db_route_write
        

class BaseMultiTenantMiddleware(object):
    signal_function = None
    signals = [db_route_read, db_route_write]
    models = None
    
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
    
    def get_models(self):
        return self.models
        
    def connect_signals(self, request, weak=False, **kwargs):
        for signal in self.get_signals():
            models = self.get_models()
            if models is None:
                signal.connect(
                    self.get_signal_function(request=request), 
                    weak=weak, 
                    dispatch_uid=self.get_dispatch_uid(request), 
                    **kwargs
                )
            else:
                for model in models:
                    signal.connect(
                        self.get_signal_function(request=request), 
                        sender=model, 
                        weak=weak, 
                        dispatch_uid=self.get_dispatch_uid(request), 
                        **kwargs
                    )
    
    def disconnect_signals(self, request, weak=False, **kwargs):
        for signal in self.get_signals():
            models = self.get_models()
            if models is None:
                signal.disconnect(weak=weak, dispatch_uid=self.get_dispatch_uid(request), **kwargs)
            else:
                for model in models:
                    signal.disconnect(weak=weak, sender=model, dispatch_uid=self.get_dispatch_uid(request), **kwargs)
        
    def process_request(self, request):
        self.connect_signals(request)
        return None
        
    def process_response(self, request, response):
        self.disconnect_signals(request)
        return response
    
    
class RequestMultiTenantMixin(object):
    @classmethod
    def get_request(cls, sender, request=None, **kwargs):
        return request
    
    def get_signal_function(self, request=None, **kwargs):
        return curry(self.get_request, request=request)


class RequestAttributeMultiTenantMixin(RequestMultiTenantMixin):        
    @classmethod
    def get_request(cls, sender, request=None, **kwargs):
        return request and request.GET.get('tenant', 'default') or None

class MultiTenantMiddleware(RequestAttributeMultiTenantMixin, BaseMultiTenantMiddleware):
    pass

from saas.multitenant.models import TenantDatabase
from django.core.exceptions import MiddlewareNotUsed

class AutoLoadMiddleware(object):
    def __init__(self):
        TenantDatabase.objects.load()
        raise MiddlewareNotUsed()
