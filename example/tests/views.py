from django.views import generic
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from saas.multidb.middleware import request_router_info
from tests.models import *
from tests.forms import TestDataForm


MODELS = [TestModel3, TestModel2, TestModel1]

class IndexView(generic.base.TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'databases': [{
                'name': db,
                'querysets': dict([(model.__name__, model.objects.using(db).all()) for model in MODELS]),
            }for db in settings.DATABASES.keys()],
            'form': TestDataForm(models=MODELS, initial={'database': self.request.GET.get('domain', 'default')}),
        })
        return context
    
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
            model_class.objects.using(form.cleaned_data['database']).create(value=form.cleaned_data['value'])
            print self.request.META['HTTP_REFERER']
            return HttpResponseRedirect(self.request.META['HTTP_REFERER'])
        return HttpResponseRedirect(self.request.get_full_path())
