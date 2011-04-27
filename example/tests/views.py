from django.views import generic
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from saas.multidb.middleware import request_router_info
from saas.multidb.models import Database

from tests.models import *
from tests.forms import TestDataForm, DatabaseForm


MODELS = [TestModel3, TestModel2, TestModel1]

#Example for multidb creation
class IndexView(generic.base.TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'settings': settings.DATABASES.keys(),
            'databases': [{
                'name': db,
                'querysets': dict([(model.__name__, model.objects.using(db if db == 'default' else db.db).all()) for model in MODELS]),
            }for db in ['default'] + list(Database.objects.all())],
            'form': TestDataForm(models=MODELS, initial={'database': self.request.GET.get('domain', 'default')}),
            'db_form': DatabaseForm(),
        })
        return context

#Example for Routing
class DetailView(generic.base.TemplateView):
    template_name = 'database.html'
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        
        context.update({
            'form': TestDataForm(models=MODELS, initial={'database': self.request.GET.get('domain', 'default')}),
            'database': request_router_info(None, self.request),
            'querysets': dict([(model_class.__name__, model_class.objects.all()) for model_class in MODELS]),
        })
        return context

class CreateView(generic.base.View):
    form_class = TestDataForm
    
    def get(self, *args, **kwargs):
        return HttpResponseRedirect(reverse('index'))
    
    def post(self, *args, **kwargs):
        form = self.form_class(data=self.request.POST, models=MODELS)
        
        if form.is_valid():
            model_class = form.cleaned_data['model']
            for i in range(form.cleaned_data['number']):
                model_class.objects.using(form.cleaned_data['database']).create(value=form.cleaned_data['value'])
            return HttpResponseRedirect(self.request.META['HTTP_REFERER'])
        return HttpResponseRedirect(self.request.get_full_path())

class CreateDBView(generic.edit.CreateView):
    model = Database
    form_class = DatabaseForm
    
    def get(self, *args, **kwargs):
        return HttpResponseRedirect(reverse('index'))
    
    def get_success_url(self):
        return reverse('index')

class DeleteDBView(generic.edit.DeleteView):
    model = Database
    form_class = DatabaseForm
    
    def get(self, *args, **kwargs):
        return HttpResponseRedirect(reverse('index'))
        
    def get_success_url(self):
        return reverse('index')
