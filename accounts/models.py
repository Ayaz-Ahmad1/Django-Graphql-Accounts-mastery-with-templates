from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User (AbstractUser):

    email = models.EmailField( max_length=255, verbose_name='email', unique=True)
    username = models.CharField( max_length=150, unique=True )    
    profile_pic = models.ImageField(blank=True, null=True, upload_to='profile_pics/')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']


