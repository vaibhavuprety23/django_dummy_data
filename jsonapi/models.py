from django.db import models

# Create your models here.
class UserProfile(models.Model):
    isActive = models.BooleanField()
    balance = models.CharField(max_length=50)
    age = models.IntegerField()
    eyeColor = models.CharField(max_length=50)
    name = models.CharField(max_length=100) 
    gender = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    
    


    