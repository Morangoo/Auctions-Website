from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import *


class CreateListingForm(forms.Form):
    title = forms.CharField()



def index(request):
    data = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "listings": data
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

def listing(request, listing_id):
    if request.method == "POST":

        f = request.POST["content"]
        print(f)

        if 'content' in request.POST:
            print('teste')

        return HttpResponseRedirect(reverse('listing', kwargs={'listing_id': listing_id}))







    listing = Listing.objects.get(pk=listing_id)

    bidlist = listing.listing_bids.values_list("value")
    #print(bidlist)


    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_bid": 4.05
    })

def category_listings(request, categoryid):
    data = Category.objects.get(id=categoryid)

    title = data.title
    listings = data.list_category.all()
    
    return render(request, "auctions/categorylistings.html", {
        "title" : title,
        "listings": listings
    })

def create_listing(request):

    
    return render(request, "auctions/createlisting.html")