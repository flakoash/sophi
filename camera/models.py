from django.db import models
from django.contrib.auth.models import User

#superuser:
#   root
#pass:
#   toor1234
# Create your models here.
class photos(models.Model):

    #user = models.ForeignKey(User,on_delete=models.CASCADE)
    photo = models.ImageField('image')

