from django.forms import ModelForm, Textarea, NumberInput, Select, TextInput, URLInput

from .models import Listing, Bid, Comment

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['item', 'min_price', 'category','image_url' , 'description']
        initial = {'category' : 'general'}
        labels = {'min_price' : 'starting price'}
        widgets = {
            'min_price' : NumberInput(attrs={"class" : "form-control"}), 
            'description' : Textarea(attrs={'class' : 'form-control'}),
            'category' : Select(attrs={"class" : "form-control"}), 
            'item' : TextInput(attrs ={"class" : "form-control"}),
            'image_url' : URLInput(attrs={"class" : "form-control"})
            }

class CommentForm(ModelForm):
        class Meta:
            model = Comment
            fields = ['text']
            labels = { 'text' : ''}
            widgets = { 'text' : Textarea(attrs={'title' : 'Your comment' , 'class' : "form-control"}) }
            help_texts = {'text' : 'Enter your comments to this listing here.'}

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        exclude = ['user', 'listing']
        widgets = {'amount' : NumberInput(attrs={'Title' : 'Your offer for this listing. It should be greate than the starting price and highest bid so far', 'class' : "form-control"}) }
        help_texts = {'text' : 'Your bid should be higher than the minimum price and highest bid so far.'}