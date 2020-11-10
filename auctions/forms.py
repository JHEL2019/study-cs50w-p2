from django.forms.models import ModelFormMetaclass
from django.forms import ModelForm, Textarea

from .models import User, Listing, Bid, Comment, Category

# Add Forms here

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['item', 'min_price', 'category','image_url' , 'description']
        initial = {'category' : 'general'}

class CommentForm(ModelForm):
        class Meta:
            model = Comment
            fields = ['text']
            widgets = { 'text' : Textarea(attrs={'cols': 80, 'rows': 20}) }

