from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', TemplateView.as_view(template_name= "index.html"), name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('account', views.account, name='account'),
   
    path('Inscription/', views.inscription, name='inscription'),
    
    path('NeedHelp/', views.need_help, name='need_help'),

    path('NeedHelp/<int:shipping_id>/', views.need_help_unique, name='need_help_unique'),

    path('GiveHelp/', views.give_help, name='give_help'),

    path('Photo/', views.photo, name='photo'),

    path('shippingList/', views.shipping_list, name='shipping_list'),

    path('shippingList/<int:shipping_id>/', views.shipping_unique, name='shipping_unique'),

    path('accounts/profile', views.ProfileView.as_view(), name="profile"),

    # Djando Auth
    path('/accounts/login', auth_views.LoginView.as_view(template_name="accounts/login.html"), name='login'),
    path('/accounts/logout', auth_views.LoginView.as_view(), name='logout')
]