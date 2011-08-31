from tenancy.base.routers import BaseTenantRouter


class MultiSchemaTenantRouter(BaseTenantRouter):
    def switch_schema(self, schema):
        from django.db import connection, transaction
        cursor = connection.cursor()        
        cursor.execute('SET search_path = %s;', [schema])
        transaction.commit_unless_managed()
        
    def db_for_read(self, model, **hints):
        tenant = self.get_tenant()
        if self.should_route(model, tenant=tenant, **hints):
            self.switch_schema(tenant)
            print 'MS READ', model.__name__, hints, tenant
        return None
        
    def db_for_write(self, model, **hints):
        tenant = self.get_tenant()
        if self.should_route(model, tenant=tenant, **hints):
            self.switch_schema(tenant)
            print 'MS WRITE', model.__name__, hints, tenant
        return None

    def allow_syncdb(self, db, model, **hints):
        tenant = self.get_tenant()
        if self.should_route(model, tenant=tenant, db=db, **hints):
            self.switch_schema(tenant)
            print 'MS SYNCDB', model.__name__, hints, tenant
        return None
