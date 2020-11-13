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
            widgets = { 'text' : Textarea(attrs={'cols': 50, 'rows': 3}) }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        exclude = ['user', 'listing']


    def clean(self):
        amount = self.cleaned_data.get('amount')
        print()
        print("Error", Bid.objects.values('listing__min_price'))
        return

        if amount <= Bid.objects.all()[0]:
            print("Error", Bid.objects.all()[0])
            raise ValidationError("Yor bid must be higher than starting price")
        return amount

    '''
    amount = IntegerField(validators=[MinValueValidator(self.objects.all()[0].values('min_price'), message="Your bid must be higher than the starting price")])
   
    def clean(self):
        amount = 
        if Bid.objects.filter(listing__min_price__gt=F('amount')):
            raise ValidationError("Yor bid must be higher than starting price")
    '''