from django.db import models
from passlib.hash import pbkdf2_sha256
# Create your models here.
class UserManager(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=256,unique=True)
    password = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    age = models.IntegerField(null=True)
    
    def verify_password(self,raw_password):
        return pbkdf2_sha256.verify(raw_password,self.password)
    

class Book(models.Model):
    isbn = models.CharField(max_length=2560,primary_key=True)
    title = models.CharField(max_length=2560)
    author = models.CharField(max_length=2560)
    year = models.IntegerField()
    publisher = models.CharField(max_length=2560)
    image_s =models.URLField()
    image_m = models.URLField()
    image_l = models.URLField()

class Rating(models.Model):
    user_id = models.ForeignKey(UserManager,on_delete=models.SET_NULL,null=True)
    isbn = models.ForeignKey(Book,on_delete=models.SET_NULL,null=True)
    rating = models.IntegerField()