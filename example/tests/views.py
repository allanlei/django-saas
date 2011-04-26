from django.views import generic
from django.conf import settings

from django.contrib.auth.models import User

from tests.models import *


class IndexView(generic.base.TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'databases': settings.DATABASES.keys(),
        })
        return context
    
class DetailView(generic.base.TemplateView):
    template_name = 'database.html'
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        
        model_classes = [User, TestModel1, TestModel2, TestModel3]
        
        
        
        context.update({
            'querysets': dict([(model_class.__name__, model_class.objects.all()) for model_class in model_classes]),
        })
        return context
