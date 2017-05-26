from django.db import models
from django.contrib.auth.models import User

#superuser:
#   root
#pass:
#   toor1234
# Create your models here.
class photos(models.Model):

    #user = models.ForeignKey(User,on_delete=models.CASCADE)
    photo = models.ImageField('image', upload_to='media/')

class UserRecomandation (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=45)
    size = models.TextField(max_length=45)
    color = models.TextField(max_length=45)
    brand = models.TextField(max_length=45)
    like = models.BooleanField()
    photo = models.TextField(max_length=45)

class Clothes (models.Model):
    brand = models.TextField(max_length=45)
    color = models.TextField(max_length=45)
    imgURL = models.TextField(max_length=45)
    outfit_recomendation = models.ManyToManyField(Outfit_recomendation)

class Wardrobe_division (models.Model):
    name = models.TextField(max_length=45)

class Type_clothe(models.Model):
    name = models.TextField(max_length=45)

class Type_clothe_category(models.Model):
    name = models.TextField(max_length=45)
    type_clothe = models.ForeignKey(Type_clothe, on_delete=models.CASCADE)

class Outfit_recomendation(models.Model):
    fecha = models.DateTimeField()
    like = models.BooleanField()

class Wardrobe_division_clothe_user(models.Model):
    wardrobe_division=models.ForeignKey(Wardrobe_division, on_delete=models.CASCADE)
    type_clothe = models.ForeignKey(Type_clothe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


