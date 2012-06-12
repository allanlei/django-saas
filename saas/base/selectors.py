from tenancy import tenants
from tenancy.base.signals import tenant_selection

class LocalThreadTenantSelectorMixin(object):
    def get_tenant(self):
        return tenants.current_tenant()

class SignalTenantSelectorMixin(object):
    def get_tenant(self):
        responses = tenant_selection.send(sender=None)
        for receiver, response in responses:
            return response
        return None
