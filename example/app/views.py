from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from models import Pizza, Topping

class HomeView(generic.base.TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            'pizzas': Pizza.objects.all(),
        })
        return context

class PizzaCreateView(generic.edit.CreateView):
    model = Pizza
    template_name = 'pizza_form.html'
    
    def get(self, *args, **kwargs):
        if not Topping.objects.exists():
            return HttpResponseRedirect(reverse('create_topping'))
        return super(PizzaCreateView, self).get(*args, **kwargs)
        
    def get_success_url(self):
        return reverse('home')

class ToppingCreateView(generic.edit.CreateView):
    model = Topping
    template_name = 'topping_form.html'

    def get_success_url(self):
        return reverse('home')
