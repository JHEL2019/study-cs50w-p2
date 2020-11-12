from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Category
from .forms import ListingForm, CommentForm, BidForm

# Add views here:

# default route Index showing all actiive listings
def index(request):
    # query set of all listings where active=True
    active_listings = Listing.objects.filter(active=True).values()
    
    # render listings with query-set
    return render(request, "auctions/index.html", {
        'listings' : active_listings
    })


# Login User
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if 'watchlist' not in request.session:
                request.session['watchlist'] = []

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

# Logout User
@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Register user
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

# New Listing
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
    
# Manipulate active listing details
def listing(request, listing_id, method=["GET", "POST"]):
    if request.method == "GET":

        # retrieve data for listing record and create additional context
        listing = Listing.objects.get(id = listing_id)
        listing_details = Listing.objects.filter(id = listing_id).values().first()

        # retrieve all comments and bids linked to this listing
        comments = listing.comment_set.all()

        # retrieve all bids sorted from highest to lowest
        bids = listing.bid_set.all().order_by('-amount')
        
        # create additional context
        listing_owner = User.objects.filter(id = listing_details['owner']).values().first()["username"]

        return render(request, "auctions/listing.html", {
            'listing' : listing_details, 
            'comments' : comments, 
            'commentform' : CommentForm(),
            'bids' : bids,
            'bidform' : BidForm(),
            'listing_owner' : listing_owner
        })
    # Processing POST request
    else:
        # data = request.POST


        # Watchlist button was pressed
        if request.POST.get("btn-watchlist"):
            num = int(request.POST['btn-watchlist'])
            # change this to use arg listring_id

            if num in request.session['watchlist']:
                 request.session['watchlist'].remove(num)
            else:
                request.session['watchlist'].append(num)
            
            request.session.save()


        # New Bid was made
        elif request.POST.get("btn-bid"):
            pass


        # New Comment was submitted
        elif request.POST.get("btn-comment"):
            print("LISTING - POST: BID:")
            print(request.POST)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment(text = form.cleaned_data['text'], listings = listing_id, users = request.user)
                comment.save

        # Listing was closed
        elif request.POST.get("btn-closed"):
            pass


        # POST request was received but cannot parsed
        else:
            return HttpResponse("User input could not be processed")
            # render(request, "auctions/listing.html", { 'message' : "User input could not be processed" })

        
        return HttpResponseRedirect("/")
