from tenancy.base.selectors import SignalTenantSelectorMixin
from tenancy.database.routers import MultiDatabaseTenantRouter

class SignalMultiDBTenantRouter(SignalTenantSelectorMixin, MultiDatabaseTenantRouter):
    pass
