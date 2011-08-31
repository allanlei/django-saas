from django.conf import settings
from django.utils.functional import curry

from tenancy import tenants
from tenancy.base.signals import tenant_selection



class LocalThreadTenantMiddleware(object):
    def process_request(self, request):
        tenants.tenant = settings.SAAS_TENANCY_FN(request)
        return None
        
    def process_response(self, request, response):
        tenants.tenant = None
        return response


class SignalTenantMiddleware(object):
    def process_request(self, request):
        tenant = settings.SAAS_TENANCY_FN(request)
        tenant_selection.connect(curry(lambda sender, **kwargs: kwargs.get('tenant', None), tenant=tenant), weak=False, dispatch_uid=request)
        return None
        
    def process_response(self, request, response):
        tenant_selection.disconnect(weak=False, dispatch_uid=request)
        return response
