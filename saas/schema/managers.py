from django.db import models


class TenantManager(models.Manager):
    def using(self, tenant, **kwargs):
        print 'MULTISCHEMA', 'switch schema to ', tenant
        return super(TenantManager, self).using(None)
