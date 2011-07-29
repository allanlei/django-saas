from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from saas.multitenant.models import TenantDatabase

from example.app.models import *

class DatabaseMixin(object):
    model = TenantDatabase
    
    def get_queryset(self):
        return super(DatabaseMixin, self).get_queryset().using('default')



class ListView(DatabaseMixin, generic.list.ListView):
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        for obj in self.object_list:
            obj.item_count = sum([model.objects.using(obj.db).count() for model in [TestModel1, TestModel2, TestModel3]])
        
        default = settings.DATABASES['default']
        default.update({
            'item_count': sum([model.objects.using('default').count() for model in [TestModel1, TestModel2, TestModel3]])
        })
        
        context.update({
            'default': default,
        })
        return context

class CreateView(DatabaseMixin, generic.edit.CreateView):
    def get_success_url(self):
        return reverse('item:list') + '?tenant=%s' % self.object.db
        
    def form_valid(self, form, **kwargs):
        tenant = form.save(commit=False)
        tenant.save(using='default')
        self.object = tenant
        return HttpResponseRedirect(self.get_success_url())

class UpdateView(DatabaseMixin, generic.edit.UpdateView):
    pass

class DeleteView(DatabaseMixin, generic.edit.DeleteView):
    pass
