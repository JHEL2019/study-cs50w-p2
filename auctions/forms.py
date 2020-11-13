# from django.db import models
# from django.db.models import F
from django.forms.fields import IntegerField
from django.forms.models import ModelFormMetaclass
from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.http.request import RAISE_ERROR

from .models import Listing, Bid, Comment

# Add Forms here

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['item', 'min_price', 'category','image_url' , 'description']
        initial = {'category' : 'general'}
        labels = {'min_price' : 'starting price'}

class CommentForm(ModelForm):
        class Meta:
            model = Comment
            fields = ['text']
            labels = { 'text' : ''}
            widgets = { 'text' : Textarea(attrs={'cols': 70, 'rows': 3}) }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        exclude = ['user', 'listing']

    