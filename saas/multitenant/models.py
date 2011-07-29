from django.db import models

from base.models import BaseTenantDatabase
from base import managers


class TenantDatabase(BaseTenantDatabase):
    objects = managers.DatabaseManager()
    
    def __unicode__(self):
        return u'%s(%s)' % (self.db, self.engine.split('.')[-1])

    @models.permalink
    def get_absolute_url(self):
        return ('tenant:detail', (), {'pk': self.pk})
