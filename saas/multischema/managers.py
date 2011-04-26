from django.db import models
from django.conf import settings

from appschema import schema

class SchemaManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)
    
    def get_current(self, check=False):
        schemaname = schema.current_schema(check)
        if schemaname not in list(getattr(settings, 'APPSCHEMA_DEFAULT_PATH', ['public'])):
            return self.get(name=schemaname)
