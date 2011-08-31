from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import views
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings


class CreateView(generic.edit.FormView):
    form_class = UserCreationForm
    template_name = 'registration/create.html'
    
    def get_success_url(self):
        return settings.LOGIN_REDIRECT_URL
        
    def form_valid(self, form, **kwargs):
        user = form.save()
        user = authenticate(username=user.username, password=form.cleaned_data['password2'])
        if user:
            user.is_superuser = True
            user.save()
            login(self.request, user)
        return super(CreateView, self).form_valid(form, **kwargs)

class LoginView(generic.edit.FormView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
        
    def get_success_url(self):
        return settings.LOGIN_REDIRECT_URL
        
    def form_valid(self, form, **kwargs):
        email = form.cleaned_data['username']
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        return HttpResponseRedirect(reverse('login'))

class LogoutView(generic.base.View):
    def dispatch(self, *args, **kwargs):
        return views.logout_then_login(*args, **kwargs)
