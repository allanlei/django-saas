from tenancy.base import managers


class TenantManager(managers.TenantManager):
    def tenant(self, tenant):
        print 'MULTIDB using %s' % tenant
        return self.using(tenant)
