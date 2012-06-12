#from django.utils.thread_support import currentThread
from threading import local


class TenantStore(local):
    tenant = None
    
    def current_tenant(self):
        return self.tenant

tenants = TenantStore()
