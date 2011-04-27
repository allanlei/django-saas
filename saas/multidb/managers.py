from django.db import models
from django.conf import settings
	
class DatabaseQueryset(models.query.QuerySet):
    def load(self):
        for db in self.all():
            db.load()
    
    def unload(self):
        for db in self.all():
            db.unload()
            
class DatabaseManager(models.Manager):
    def get_query_set(self):
		return DatabaseQueryset(self.model)
		
    def __getattr__(self, attr, *args):
        return getattr(self.get_query_set(), attr, *args)
    
    def unload(self, name):
        if name in settings.DATABASES:
            self.get(db=name).unload()
