from django.conf import settings

from signals import db_route_read, db_route_write
#from saas.multidb.utils import ModelRoutingRegistry

class RequestDBRouter(object):
#    def __init__(self):
#        reg = ModelRoutingRegistry()
#        models = getattr(settings, 'MODEL_ROUTABLE', [])
#        for model in models:
#            reg.add_model(model)
            
    def db_for_read(self, model, **hints):
        responses = db_route_read.send(sender=model, **hints)
        if responses:
            for response in responses:
                if response[1] is not None:
                    return response[1]
    
    def db_for_write(self, model, **hints):
        responses = db_route_write.send(sender=model, **hints)
        if responses:
            for response in responses:
                if response[1] is not None:
                    return response[1]
