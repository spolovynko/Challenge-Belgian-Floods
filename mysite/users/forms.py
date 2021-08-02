from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    need_help = forms.BooleanField(initial=False)
    give_help = forms.BooleanField(initial=False)



    class Meta:
        model = User
        fields =['username', 'first_name', 'last_name', 'need_help', 'give_help', 'email', 'password1', 'password2']

class UploadFileForm(forms.Form):
    file = forms.ImageField(max_length=Any)