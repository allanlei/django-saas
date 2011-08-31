#from django.db import models

#import managers

#class MultiSchemaTenantMixin(models.Model):
#    tenancy = managers.MultiSchemaTenantManager()

#    class Meta:
#        abstract = True

#    class TenantMeta:
#        route_from_field = None
#        route_to_model = None
#        route_to_field = None

#    def get_routing_kwargs(self):
#        return {}

#    def enter(self):
#        raise NotImplementedError()

#    def exit(self):
#        raise NotImplementedError()
