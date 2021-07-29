from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .utils import Constantes
from .models import Objet
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    """ or return render(request, 'index.html') """
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def inscription(request):
    pass

def shipping(request):
    return HttpResponse("Shipping page")

def need_help(request):
    return render(request, 'need_help.html') 

def need_help_unique(request, shipping_id):
    list_objects= Objet.objects.filter(available=True)
    available = dict()
    for objet in Constantes.type_object.keys():
        available[objet] = list_objects.filter(category=Constantes.type_object[objet]).count()
    print(available)
    return render(request, 'new_package.html', {"type_object": Constantes.type_object,
     "type_food": Constantes.type_food, "type_housing": Constantes.type_housing, "available_dict": available}) 

def give_help(request):
    pass

def photo(request):
    pass

def shipping_list(request):
    pass

def shipping_unique(request):
    pass

def about(request):
    return render(request, 'about.html') 

def contact(request):
    return render(request, 'contact.html') 

def account(request):
    return render(request, 'account.html') 
    
# Create your views here.

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
