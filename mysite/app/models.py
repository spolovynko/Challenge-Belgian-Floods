from django.db import models

class Utilisateur(models.Model):
    name = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    type = models.IntegerField(default=0)
    email = models.EmailField()
    mdp = models.CharField(max_length=200, default="***")

    def __str__(self) -> str:
        return self.name


class Objet(models.Model):
    receiving_date = models.DateTimeField(auto_now_add=True)
    sending_date = models.DateTimeField('date published')
    category = models.IntegerField(default=0)
    sender = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.category) + str(self.id)

class Shipping(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    sending_date =  models.DateTimeField(auto_now_add=True)
    state = models.CharField(default=0, max_length=200)

    def __str__(self) -> str:
        return str(self.utilisateur) + str(self.id)

class Objet_Shipping(models.Model):
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    objet = models.ForeignKey(Objet, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self) -> str:
        return str(self.shipping)



