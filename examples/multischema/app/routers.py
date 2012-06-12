from tenancy.base.selectors import SignalTenantSelectorMixin
from tenancy.database.routers import MultiDatabaseTenantRouter

class SignalMultiDBTenantRouter(SignalTenantSelectorMixin, MultiDatabaseTenantRouter):
    pass
    
    
from tenancy.base.selectors import SignalTenantSelectorMixin
from tenancy.schema.routers import MultiSchemaTenantRouter

class SignalMultiSchemaTenantRouter(SignalTenantSelectorMixin, MultiSchemaTenantRouter):
    pass
