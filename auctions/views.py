from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms


from operator import attrgetter

from .models import *


class CreateListingForm(forms.Form):
    title = forms.CharField()

    data = Category.objects.all()
    Categories = []

    for category in data:
        Categories.append((category.id, category.title))

    category = forms.ChoiceField(widget=forms.Select, choices=Categories)
    imageurl = forms.URLField()
    description = forms.CharField(widget=forms.Textarea())
    starting_bid = forms.DecimalField(max_digits=10, decimal_places=2)


def index(request):
    data = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "listings": data,
        "title": "Active Listings"
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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

def category_list(request):
    list = Category.objects.all()

    return render(request, "auctions/categories.html", {
        "list": list
    })


@login_required
def listing(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        user = request.user

        if 'placecomment' in request.POST:
            # User, content, Listing
            comment = Comment(user=user, content=request.POST["content"], listing=listing)
            comment.save()

        elif 'placebid' in request.POST:
            # new bid value
            value = request.POST["bidvalue"]

            # Value checking 
            if float(value) > listing.starting_bid and float(value) > listing.current_bid:
                # Create a new bid
                bid = Bid(value=value, user=user, listing=listing)
                listing.current_bid = value
                bid.save()
                listing.save()

            elif float(value) < listing.starting_bid:
                # Error new value need to be higher than the starting bid
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "user": request.user,
                    "message": "A new bid needs to be higher than the starting price."
                })
            else:
                # Error new value need to be higher than the current bid
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "user": request.user,
                    "message": "A new bid needs to be higher than the current bid."
                })

        elif 'closelisting' in request.POST:
            listing.active = False
            winnerbid = max(listing.listing_bids.all(), key=attrgetter('value'))

            # Code to set the winner
            listing.winner = winnerbid.user
            listing.save()

            return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))
        elif 'watchlistadd' in request.POST:
            listing.watchlist.add(user)
            return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))

        elif 'watchlistremove' in request.POST:
            listing.watchlist.remove(user)
            return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))


        return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))



    listing = Listing.objects.get(pk=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "user": request.user
    })

def category_listings(request, categoryid):
    data = Category.objects.get(id=categoryid)

    title = data.title
    listings = data.list_category.all()
    
    return render(request, "auctions/index.html", {
        "title" : title,
        "listings": listings
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)

        if form.is_valid():
            print("teste")
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            image = form.cleaned_data["imageurl"]
            category = Category.objects.get(id=form.cleaned_data["category"])
            starting_bid = form.cleaned_data["starting_bid"]
            seller = request.user

            listing = Listing(title=title, description=description, image=image, category=category, starting_bid=starting_bid, active=1, seller=seller)
            listing.save()

            return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing.id}))

        return render(request, "auctions/createlisting.html", {
            "createform": CreateListingForm(),
            "message": "Invalid data on the form"
        })
    
    return render(request, "auctions/createlisting.html", {
        "createform": CreateListingForm()
    })

@login_required
def watchlist(request):
    list = request.user.user_watchlist.all()

    return render(request, "auctions/index.html", {
        "listings": list,
        "title": "Watchlist"
    })

@login_required
def closed_listings(request):
    list = request.user.user_listings.filter(active=False)

    return render(request, "auctions/closedlistings.html", {
        "listings": list,
        "title": "Closed Listings"
    })

@login_required
def won_listings(request):
    list = request.user.user_wins.all()

    return render(request, "auctions/closedlistings.html", {
        "listings": list,
        "title": "Won Listings"
    })
