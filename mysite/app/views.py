from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .utils import Constantes
from .models import Objet, Utilisateur, Shipping, Objet_Shipping
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    """ or return render(request, 'index.html') """
    print(request.user)
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def inscription(request):
    pass

def shipping(request):
    return HttpResponse("Shipping page")

def need_help(request):
    user = Utilisateur.objects.first()

    if request.method == 'POST':
        s = Shipping(utilisateur = user)
        s.save()
        for key, value in request.POST.dict().items():
            print(value, type(value))
            if value != "0":
                if key in Constantes.type_food.keys():
                    print("food",  Constantes.type_object[key])
                    o = Objet.objects.filter(category = Constantes.type_food[key])[0]
                    o_s = Objet_Shipping(shipping = s, objet = o, quantity = value)
                    
                elif key in Constantes.type_object.keys():
                    print("object",  Constantes.type_object[key])
                    o = Objet.objects.filter(category = Constantes.type_object[key])[0]
                    o_s = Objet_Shipping(shipping = s, objet = o, quantity = value)
                else:
                    continue
                o.available = False
                o.save()
                o_s.save()
            
    
    list_shipping= Shipping.objects.filter(utilisateur=user)
    return render(request, 'need_help.html', {"utilisateur": user, "list_shipping": list_shipping}) 

def need_help_unique(request):
    list_objects= Objet.objects.filter(available=True)
    available = dict()
    for objet in Constantes.type_object.keys():
        available[objet] = list_objects.filter(category=Constantes.type_object[objet]).count()
    for key, value in Constantes.type_food.items():
        available[key] = list_objects.filter(category=value).count()
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
