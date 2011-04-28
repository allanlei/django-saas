from django.utils.functional import curry
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed

from saas.multidb.signals import db_route_read, db_route_write
from saas.multidb.models import Database


class ModelRoutingMiddleware(object):
    @classmethod
    def request_router_info(cls, sender, request=None, **kwargs):
        if request:
            return request.REQUEST.get('domain', 'default')
        
    def get_signal_function(self, **kwargs):
        return curry(self.request_router_info, **kwargs)
    
    def process_request(self, request):
        db_route_read.connect(self.get_signal_function(request=request), weak=False, dispatch_uid=request)
        db_route_write.connect(self.get_signal_function(request=request), weak=False, dispatch_uid=request)
        return None
    
    def process_response(self, request, response):
        db_route_read.disconnect(weak=False, dispatch_uid=request)
        db_route_write.disconnect(weak=False, dispatch_uid=request)
        return response



class AutoLoadMiddleware(object):
    def __init__(self):
        Database.objects.all().load()
        raise MiddlewareNotUsed
