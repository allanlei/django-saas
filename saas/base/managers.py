#from django.db import models

#from tenancy.middleware import tenants



#class TenantManager(models.Manager):
#    def all(self, *args, **kwargs):
#        return self.current_tenant().all(*args, **kwargs)
#        
#    def filter(self, *args, **kwargs):
#        return self.current_tenant().filter(*args, **kwargs)
#    
#    def get_current_tenant(self):
#        tenant = tenants.current_tenant()
##        print 'TENANT ', tenant
#        return tenant
#        
#    def tenant(self, tenant):
#        raise NotImplementedError()

#    def current_tenant(self):
#        tenant = self.get_current_tenant()
#        return self.tenant(tenant)
