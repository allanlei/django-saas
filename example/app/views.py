from django.views import generic
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.forms import models as model_forms

from saas.multitenant.models import TenantDatabase

from models import *


class ItemMixin(object):        
    def get_queryset(self):
        model = self.request.REQUEST.get('model', 'TestModel1').lower()
        print model
        if model == 'TestModel1'.lower():
            self.model = TestModel1
        elif model == 'TestModel2'.lower():
            self.model = TestModel2
        elif model == 'TestModel3'.lower():
            self.model = TestModel3
        return super(ItemMixin, self).get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super(ItemMixin, self).get_context_data(**kwargs)
        context.update({
            'tenant': self.request.GET.get('tenant', 'default'),
        })
        return context
    
class ListView(ItemMixin, generic.base.TemplateView):
    template_name = 'list.html'
    
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'form': model_forms.modelform_factory(TestModel1),
            'models': dict([(model._meta.object_name, model.objects.all()) for model in [TestModel1, TestModel2, TestModel3]])
        })
        return context

class CreateView(ItemMixin, generic.edit.CreateView):
    template_name = 'form.html'
    
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context.update({
            'models': [model._meta.object_name for model in [TestModel1, TestModel2, TestModel3]],
        })
        return context
    
    def get_success_url(self):
        return '%s?tenant=%s' % (reverse('item:list'), self.request.GET.get('tenant', ''))
