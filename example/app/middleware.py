from saas.multitenant.base.middleware import BaseMultiTenantMiddleware, RequestMultiTenantMixin


class MultiTenantMiddleware(RequestMultiTenantMixin, BaseMultiTenantMiddleware):
    @classmethod
    def get_request(cls, sender, request=None, **kwargs):
        return request and request.GET.get('tenant', None) or None
