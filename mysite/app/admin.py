from django.contrib import admin
from .models import Objet, Utilisateur
# Register your models here.

admin.site.register([Utilisateur, Objet])