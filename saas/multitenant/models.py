from base import BaseTenantDatabase

class TenantDatabase(BaseTenantDatabase):
    def __unicode__(self):
        return u'%s(%s)' % (self.db, self.engine.split('.')[-1])
