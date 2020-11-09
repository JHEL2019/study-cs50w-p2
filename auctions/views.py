from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.forms.models import ModelFormMetaclass
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from .models import User, Listing, Bid, Comment, Category


# Add Forms here (alternatively move to forms.py):
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['item', 'min_price', 'category','image_url' , 'description']
        initial = {'category' : 'general'}


# Add views here:
def index(request):
    # query set of all listings where active=True
    active_listings = Listing.objects.filter(active=True).values()
    
    # render listings with query-set
    return render(request, "auctions/index.html", {
        'listings' : active_listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if not request.sessions['watchlist']:
                request.sessions['watchlist']=[]
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required()
def new_listing(request, method = ["GET", "POST"]):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            newlisting = Listing(item = form.cleaned_data['item'], min_price = form.cleaned_data['min_price'],description = form.cleaned_data['description'], image_url = form.cleaned_data['image_url'], owner = request.user.id, category = form.cleaned_data['category'])
            
            newlisting.save()
        return HttpResponseRedirect("/")
    else:
        return render(request, 'auctions/new_listing.html', {
            'form' : ListingForm
        })
    
   
def listing(request, listing_id, method=["GET", "POST"]):
    if request.method == "GET":
        # retrieve data for listing record and create context
        this_listing = Listing.objects.filter(id = listing_id).values().first()
        

        print(this_listing)

        # retrieve all comments lined to this listing
        comments = {}

        # retrieve all bids sorted from highest to lowest
        bids = {}
        

        return render(request, "auctions/listing.html", {
            'listing' : this_listing, 
            'comments' : comments, 
            'bids' : bids
        })
    else:
        return HttpResponseRedirect("/")
