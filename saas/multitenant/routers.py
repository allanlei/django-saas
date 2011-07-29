from django.conf import settings

from saas.multitenant.base import signals

class MultiTenantRouter(object):
    def get_db_from_signal(self, signal, model, **hints):
        responses = signal.send(sender=model, **hints) or []
        for response in responses:
            if response[1] is not None:
                return response[1]
    
    def get_read_signal(self):
        return signals.db_route_read
    
    def get_write_signal(self):
        return signals.db_route_write
        
    def db_for_read(self, model, **hints):
        return self.get_db_from_signal(self.get_read_signal(), model, **hints)
        
    def db_for_write(self, model, **hints):
        return self.get_db_from_signal(self.get_write_signal(), model, **hints)
