from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Category
from .forms import ListingForm, CommentForm, BidForm

# default route Index showing all active listings
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
            user = User.objects.get(pk=request.user.id)
            print(f"user id '{user.id}' and user name '{user.username}'.'")

            newlisting = Listing(item = form.cleaned_data['item'], min_price = form.cleaned_data['min_price'],description = form.cleaned_data['description'], image_url = form.cleaned_data['image_url'], category = form.cleaned_data['category'])
            
            print("newlisting:", newlisting)
            
            newlisting.save()
            print("user:", user)

            newlisting.users.set([user])
            print("newlistings complete")     
        return HttpResponseRedirect("/")
    else:
        return render(request, 'auctions/new_listing.html', {
            'form' : ListingForm
        })


# Listing Details
def listing(request, listing_id, method=["GET", "POST"]):
    
    # Retrieve listing object and use it to retrieve various QuerySets
    listing = Listing.objects.get(id = listing_id)
    message = ''
    
    if request.method == "GET":
        print("processing Listing via GET")
      
        # Retrieve all details of this listing
        listing_details = Listing.objects.filter(id = listing_id).values('id', 'item', 'min_price', 'description', 'createdate', 'image_url', 'active', 'category', 'users__id', 'users__username')[0]
        
        # Retrieve all comments and bids linked to this listing
        comments = listing.comment_set.values('text', 'createdate', 'user__username')

        # Retrieve highest bid
        try:
            bid_max = listing.bid_set.values('amount', 'user__id', 'user__username').order_by('-amount')[0]
        except:
            bid_max={}
        
        # Render listings view
        return render(request, "auctions/listing.html", {
            'listing' : listing_details, 
            'comments' : comments, 
            'commentform' : CommentForm(),
            'bid_max' : bid_max,
            'bidform' : BidForm(),
        })
 
    # Processing POST request
    else:
        print("processing Listing via POST")

        # Watchlist button was pressed
        if request.POST.get("btn-watchlist"):
            num = int(request.POST['btn-watchlist'])
            if num in request.session['watchlist']:
                 request.session['watchlist'].remove(num)
            else:
                request.session['watchlist'].append(num)
            request.session.save()

        # New Bid was made
        elif request.POST.get("btn-bid"):
            form = BidForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                amount_min = listing.min_price
                try:
                    amount_max = listing.bid_set.values('amount').order_by('-amount')[0]
                    print("amount_max:", amount_max)
                except:
                    message = 'Bid amount must be greater than starting price as well as highest bid so far.'
                    amount_max['amount'] = 0
                    

                # Validation of bid amount 
                print('amount:', amount)
                print('starting price', amount_min)
                print("amount max", amount_max['amount'])
                if amount > amount_min > amount_max['amount']:
                    # save is validation was successful
                    print('amount is VALID')
                    bid = Bid(amount = amount, listing = Listing.objects.get(pk=listing_id), user = request.user)
                    bid.save()
                else:
                    print("amount invalid")
                    message = 'Bid amount must be greater than starting price as well as highest bid so far.'
 
        # New Comment was submitted
        elif request.POST.get("btn-comment"):
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment(text = form.cleaned_data['text'], listings = Listing.objects.get(pk=listing_id), user = request.user)
                comment.save()

        # Listing was closed
        elif request.POST.get("btn-closed"):
            listing = Listing.objects.get(id = listing_id)
            listing.active = False
            listing.save()
            return HttpResponseRedirect("/")

        # POST request was received but cannot be parsed
        else:
            return HttpResponse("User input could not be processed")

        # Render the Listing-view again to allow User further interaction
        return HttpResponseRedirect(reverse('listing', args=(listing_id,)))


# Watchlist showing all listings in session-watchlist
@login_required()
def watchlist(request):
    # query set of all listings where active=True
    try:
        listings = Listing.objects.filter(pk__in=request.session['watchlist']).values()
    except:
        listings = {}

    # render listings with query-set
    return render(request, "auctions/index.html", {
        'listings' : listings
    })


# Categories available in Auctions
def categories(request):
    categories = Category.objects.all()
    
    return render(request, "auctions/categories.html", {
        'categories' : categories
    })


# Listings shown by category
def category_view(request, category):
    listings = Listing.objects.filter(category = category)
    
    return render(request, "auctions/category.html", {
        'listings' : listings
    })

