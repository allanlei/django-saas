from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class BaseTenantRouter(object):
    def get_tenant(self):
        raise NotImplementedError()

    def get_public_models(self):
        if not hasattr(self, 'public_models'):
            from django.db.models import get_model
            if hasattr(settings, 'SAAS_TENANCY_PUBLIC'):
                public_models = [get_model(*model.split('.')) for model in settings.SAAS_TENANCY_PUBLIC]
            else:
                public_models = []
            
            if hasattr(settings, 'SAAS_TENANCY_MODEL'):
                if settings.SAAS_TENANCY_MODEL is not None:
                    tenant_model = get_model(*settings.SAAS_TENANCY_MODEL)
                    if tenant_model not in public_models:
                        public_models.append(tenant_model)
            else:
                raise ImproperlyConfigured('Must specify SAAS_TENANCY_MODEL as a model or None')
                
            self.public_models = public_models
        return self.public_models

    def get_private_models(self):
        if not hasattr(self, 'private_models'):
            from django.db.models import get_model, get_models
            if hasattr(settings, 'SAAS_TENANCY_PRIVATE') :
                private_models = [get_model(*model.split('.')) for model in settings.SAAS_TENANCY_PRIVATE]
            else:
                private_models = get_models()
            
            private_models = list(set(private_models) - set(self.get_public_models()))
            self.private_models = private_models
        return self.private_models        
        
    def should_route(self, model, **kwargs):
        private_models = self.get_private_models()
        return kwargs.get('tenant', None) is not None and model in private_models

    def db_for_read(self, model, **hints):
        raise NotImplementedError()
        
    def db_for_write(self, model, **hints):
        raise NotImplementedError()

#    def allow_syndb(self, db, model):
#        if self.should_route(model, db=db):
#            print 'T SYNCDB', db, model.__name__, self.get_tenant()
#            return self.get_tenant()
#        return None
