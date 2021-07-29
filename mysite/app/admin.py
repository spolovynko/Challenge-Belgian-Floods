from django.contrib import admin
from .models import Objet, Utilisateur, Shipping, Objet_Shipping
# Register your models here.

admin.site.register([Utilisateur, Objet, Shipping, Objet_Shipping])