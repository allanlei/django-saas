class ModelRoutingRegistry(object):
    _registry = []
    _requires_conversion = False
        
    def add_model(self, model):
        reg = self.__class__._registry
        
        if isinstance(model, str):
            self.__class__._requires_conversion = True
            
        if model not in reg:
            reg.append(model)
    
    def clean(self):
        from django.db.models import get_model
        reg = self.__class__._registry
        
        for index, model in enumerate(reg):
            if isinstance(model, str):
                reg[index] = get_model(*model.split('.'))
        self.__class__._registry = reg
        
    def get_models(self):
        if self.__class__._requires_conversion:
            self.clean()
        return self.__class__._registry
        
    def __contains__(self, model):
        return model in self.__class__._registry



class ModelRoutingField(object):
    def contribute_to_class(self, model, field):
        reg = ModelRoutingRegistry()
        reg.add_model(model)
