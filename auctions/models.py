from django.contrib.auth.models import AbstractUser
from django.db import models
import os
from django.conf import settings
from django.db.models.deletion import DO_NOTHING, PROTECT, SET_DEFAULT

# def images_path():
#    return os.path.join(settings.MEDIA_ROOT, 'auction')

# Add your models here:

class User(AbstractUser):
    listings = models.ManyToManyField('Listing', through='Bid')
    
    #def __str__(self):
    #    return f"{self.id}: {self.name}"


class Listing(models.Model):
    item = models.CharField(max_length=60)
    min_price = models.IntegerField()
    # image = models.ImageField(upload_to = images_path())
    description = models.TextField()
    createdate = models.DateTimeField(auto_now=True)
    updatedate = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(default = '', blank=True)
    active = models.BooleanField(default=True)
    owner = models.IntegerField(default='0')
    category = models.ForeignKey('Category', default='1', on_delete=SET_DEFAULT, related_name='listing')
    users = models.ManyToManyField('User', through='Bid')
    comments = models.ForeignKey('Comment', default='', null=True, blank=True, on_delete=models.SET_NULL, related_name='listings')

    def __str__(self):
        return f"{self.id}: {self.description} - created: {self.createdate}, updated: {self.updatedate}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.IntegerField()


class Comment(models.Model):
    text = models.CharField(max_length=150, blank=True)
    createdate = models.DateTimeField(auto_now=True)
    users = models.ForeignKey('User', blank=True, on_delete=models.CASCADE, related_name='comments')


class Category(models.Model):
    category = models.CharField(max_length=25, default='general')

    def __str__(self):
        return f"{self.category}"

