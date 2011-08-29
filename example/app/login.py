from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views
from django.contrib.auth import authenticate, login
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
            login(self.request, user)
        return super(CreateView, self).form_valid(form, **kwargs)

class LoginView(generic.base.View):
    def dispatch(self, *args, **kwargs):
        return views.login(*args, **kwargs)

class LogoutView(generic.base.View):
    def dispatch(self, *args, **kwargs):
        return views.logout_then_login(*args, **kwargs)
