from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .utils import Constantes
from .models import Objet, Utilisateur, Shipping, Objet_Shipping
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


from tensorflow import keras
import tensorflow as tf
from users.forms import UploadFileForm

from django.shortcuts import render
from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings 
from tensorflow.python.keras.backend import set_session
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import decode_predictions
import matplotlib.pyplot as plt
import numpy as np
from keras.applications import vgg16
import datetime
import traceback
import time

def index(request):
    """ or return render(request, 'index.html') """
    print(request.user)
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def inscription(request):
    pass

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
    return render(request, 'give_help.html') 

def photo(request):
    
    if  request.method == "POST":
        
        f=request.FILES['sentFile'] # here you get the files needed
        response = {}
        file_name = "pic.jpg"
        file_name_2 = default_storage.save(file_name, f)
        file_url = default_storage.url(file_name_2)
        file_url = "C:\\Users\\jerem\\OneDrive\\Bureau\\NoMoreNaked\\Challenge-Belgian-Floods\\mysite\\media\\"+file_name_2
        original = load_img(file_url, target_size=(224, 224))
        numpy_image = img_to_array(original)
        
        image_batch = np.expand_dims(numpy_image, axis=0)
        # prepare the image for the VGG model
        processed_image = vgg16.preprocess_input(image_batch.copy())
        
        # get the predicted probabilities for each class
        with settings.GRAPH1.as_default():
            set_session(settings.SESS)
            VGG_MODEL = vgg16.VGG16(weights="imagenet")
            predictions=VGG_MODEL.predict(processed_image)
       
        label = decode_predictions(predictions)
        label = list(label)[0]
        response['name'] = str(label)
        return render(request,'photo.html',response)
    else:
        
        return render(request,'photo.html')

def result_photo(request):
    if  request.method == "POST":
        f=request.FILES['sentFile'] # here you get the files needed
        response = {}
        file_name = "pic.jpg"
        file_name_2 = default_storage.save(file_name, f)
        file_url = default_storage.url(file_name_2)
        original = load_img(file_url, target_size=(224, 224))
        numpy_image = img_to_array(original)
        

        image_batch = np.expand_dims(numpy_image, axis=0)
        # prepare the image for the VGG model
        processed_image = vgg16.preprocess_input(image_batch.copy())
        
        # get the predicted probabilities for each class
        with settings.GRAPH1.as_default():
            set_session(settings.SESS)
            predictions=settings.VGG_MODEL.predict(processed_image)
       
        label = decode_predictions(predictions)
        label = list(label)[0]
        response['name'] = str(label)
        return render(request,'photo.html',response)
    else:
        return render(request,'photo.html')
    '''print("debut result view")
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        f = request.FILES["file"]
        with open('photo.jpg', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            
    else:
        form = UploadFileForm()
        image = "coucou"
    
    image = 
    
    image_resized = tf.image.resize(image, [96, 96])
    print("apres resize")
    model = keras.models.load_model('Model MobileNet') 
    print("avant prediction")
    
    prediction = model.predict(image_resized)

    print("prediction", prediction)

    return render(request, 'photo.html')'''
    

def shipping_list(request):
    liste_shipping = Shipping.objects.filter(state='pending').order_by('sending_date')
    print("size shipping_list:", len(liste_shipping))
    return render(request, 'shipping_list.html', {"liste_shipping": liste_shipping})

def shipping_unique(request, shipping_id):
    package = Shipping.objects.get(pk=shipping_id)
    items = Objet_Shipping.objects.filter(shipping = package)
    item_str = dict()
    for item in items:
        cat = str(item.objet)[:3]
        print("cat", cat, type(cat))
        for key, value in Constantes.type_object.items():
            print("value", value, type(value))
            if str(value) == cat:
                item_str[key] = item.quantity
    print(item_str)
    user = package.utilisateur

    return render(request, 'shipping_unique.html', {"user": user, "user_adresse": user.adresse, "items":item_str})

def about(request):
    return render(request, 'about.html') 

def contact(request):
    return render(request, 'contact.html') 

def account(request):
    return render(request, 'account.html') 
    
# Create your views here.

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
