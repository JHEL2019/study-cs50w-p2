from django.conf import settings

from django.db import models
from django.db.models.deletion import DO_NOTHING, PROTECT, SET_DEFAULT
from django.contrib.auth.models import AbstractUser
from django.db.models.expressions import OrderBy

# User
class User(AbstractUser):
    listings = models.ManyToManyField('Listing', through='Bid')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.id}: {self.username}"


# Listing
class Listing(models.Model):
    item = models.CharField(max_length=60)
    min_price = models.IntegerField()
    description = models.TextField()
    createdate = models.DateTimeField(auto_now=True)
    image_url = models.URLField(default = '', blank=True)
    active = models.BooleanField(default=True)
    owner = models.IntegerField(default='1')
    category = models.ForeignKey('Category', default='1', on_delete=SET_DEFAULT, related_name='listing')
    users = models.ManyToManyField('User', through='Bid')

    def __str__(self):
        return f"{self.id}: {self.item} - status 'active': {self.active} - owner: {self.owner}"


# Bid
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.user} bid for {self.listing} the amout of {self.amount}"


# Comment
class Comment(models.Model):
    text = models.CharField(max_length=150, blank=True)
    # listing = models.IntegerField()
    createdate = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('User', blank=True, on_delete=models.CASCADE)
    listings = models.ForeignKey('Listing', default=None, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}: by user {self.user} created on {self.createdate}"


# Category
class Category(models.Model):
    category = models.CharField(max_length=25, default='general')

    def __str__(self):
        return f"{self.category}"
