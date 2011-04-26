from django.conf import settings

from signals import db_route_read, db_route_write

class RequestRouter(object):
    def get_db_from_signal(self, signal, model, **hints):
        responses = signal.send(sender=model, **hints)
        if responses:
            for response in responses:
                if response[1] is not None:
                    return response[1]
                    
    def db_for_read(self, model, **hints):
        return self.get_db_from_signal(db_route_read, model, **hints)
    
    def db_for_write(self, model, **hints):
        return self.get_db_from_signal(db_route_write, model, **hints)
