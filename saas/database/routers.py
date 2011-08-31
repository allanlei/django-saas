from tenancy.base.routers import BaseTenantRouter

class MultiDatabaseTenantRouter(BaseTenantRouter):
    def db_for_read(self, model, **hints):
        tenant = self.get_tenant()
        if self.should_route(model, tenant=tenant, **hints):
            print '(MDB) READ\t', model, hints, '\t', tenant
            return tenant
        return None
        
    def db_for_write(self, model, **hints):
        tenant = self.get_tenant()
        if self.should_route(model, tenant=tenant, **hints):
            print '(MDB) WRITE\t', model, hints, '\t', tenant
            return tenant
        return None
