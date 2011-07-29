from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class CustomQuerysetMixin(object):
    queryset_class = None
    
    def __init__(self, *args, **kwargs):
        if self.queryset_class is None:
            self.queryset_class = kwargs.pop('queryset_class', None)
        super(CustomQuerysetMixin, self).__init__(*args, **kwargs)
    
    def get_queryset_class(self):
        if self.queryset_class:
            qs = self.queryset_class
        else:
            raise ImproperlyConfigured('Provide queryset_class or override get_queryset_class().')
        return qs

    def get_query_set(self):
        return self.get_queryset_class()(self.model)

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)
            
            

class DatabaseQueryset(models.query.QuerySet):
    def load(self):
        for db in self.all():
            db.load()
    
    def unload(self):
        for db in self.all():
            db.unload()
            
class DatabaseManager(CustomQuerysetMixin, models.Manager):
    queryset_class = DatabaseQueryset
