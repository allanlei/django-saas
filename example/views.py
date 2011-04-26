from django.views import generic
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from saas.multidb.middleware import request_router_info

from models import TestData
from forms import *

import urllib

class ListView(generic.base.TemplateView):
    template_name = 'create.html'
    
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context.update({
            'users': User.objects.all(),
            'testdata': TestData.objects.all(),
            'defaults': {
                'testdata': TestData.objects.using('default').all(),
                'users': User.objects.using('default').all(),
            },
            'db': request_router_info(None, self.request),
            
            'user_form': UserForm(),
            'testdata_form': TestDataForm(),
        })
        return context
    
    
    
    
class UserCreateView(generic.edit.FormView):
    form_class = UserForm
    
    def get_success_url(self):
        return '%s?%s' % (reverse('list'), urllib.urlencode(self.request.GET))
        
    def form_valid(self, form):
        User.objects.create(username=form.cleaned_data['value'])
        return super(UserCreateView, self).form_valid(form)

class TestDataCreateView(generic.edit.FormView):
    form_class = TestDataForm
    
    def get_success_url(self):
        return '%s?%s' % (reverse('list'), urllib.urlencode(self.request.GET))
        
    def form_valid(self, form):
        TestData.objects.create(name=form.cleaned_data['value'])
        return super(TestDataCreateView, self).form_valid(form)
