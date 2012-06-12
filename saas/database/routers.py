from tenancy.base.routers import BaseTenantRouter

import logging

logger = logging.getLogger('tenancy')

class MultiDatabaseTenantRouter(BaseTenantRouter):
    def db_for_read(self, model, **hints):
        tenant = self.get_tenant()
        if self.should_route(model, tenant=tenant, **hints):
            logger.info('READ\t%s\t%s %s ' % (model.__name__, hints, tenant))
            return tenant
        return None
        
    def db_for_write(self, model, **hints):
        tenant = self.get_tenant()
        if self.should_route(model, tenant=tenant, **hints):
            logger.info('WRITE\t%s\t%s %s ' % (model.__name__, hints, tenant))
            return tenant
        return None
