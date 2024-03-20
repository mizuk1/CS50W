from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

from django.utils.datastructures import MultiValueDictKeyError


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
    

@login_required(login_url='login')
def create(request):
    if request.method == "POST":
        try:
            owner = request.user
            title = request.POST["title"]
            description = request.POST["description"]
            starting_bid = request.POST["bid"]
            url = request.POST["url"]
            category = Category.objects.get(name=request.POST["category"])
            listing = Listing(
                owner=owner,
                title=title,
                description=description,
                current_price=starting_bid,
                starting_bid=starting_bid,
                image_url=url,
                is_active=True,
                winner=None,
                category=category
            )
            listing.save()
        except MultiValueDictKeyError:
            return HttpResponseRedirect(reverse('auctions:create'))
        except ValueError as e:
            return HttpResponseRedirect(reverse('auctions:create'))
        
        return render(request, "auctions/create.html", {
            "message": "Listing saved successfully"
        })
    else:
        return render(request, "auctions/create.html", {
            "categories": Category.objects.all()
        })


def listing(request, listing_id):
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(id=listing_id),
        "comments": Comment.objects.filter(listing=Listing.objects.get(pk=listing_id))
    })


@login_required(login_url='login')
def watch_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    if listing not in request.user.watchlist.all():
        user.watchlist.add(listing)
    return HttpResponseRedirect(reverse('auctions:listing', args=(listing_id,)))


@login_required(login_url='login')
def unwatch_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    if listing in user.watchlist.all():
        user.watchlist.remove(listing)
    return HttpResponseRedirect(reverse('auctions:listing', args=(listing_id,)))


@login_required(login_url='login')
def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    listing.is_active = False
    listing.winner = listing.bidder
    listing.save()
    return HttpResponseRedirect(reverse('auctions:listing', args=(listing_id,)))


@login_required(login_url='login')
def bid(request, listing_id):
    if request.method == "POST":
        try:
            new_bid = float(request.POST["bid"])
            listing = Listing.objects.get(pk=listing_id)

            if new_bid > float(listing.current_price):
                listing.current_price = new_bid
                bid = Bid(
                    price=new_bid,
                    listing=listing,
                    bidder=request.user
                )
                bid.save()
                listing.current_price = new_bid
                listing.bidder = request.user
                listing.save()
            else:
                return render(request, "auctions/listing.html", {
                    "listing": Listing.objects.get(id=listing_id),
                    "message": "Bid must be greater than any other bids that have been placed."
                })
        except Exception:
            return HttpResponseRedirect(reverse('auctions:listing', args=(listing_id,)))
    return HttpResponseRedirect(reverse('auctions:listing', args=(listing_id,)))


@login_required(login_url='login')
def comment(request, listing_id):
    if request.method == "POST":
        try:
            commentary = request.POST["commentary"]
            user = request.user
            listing = Listing.objects.get(pk=listing_id)
            comment = Comment(
                user=user,
                commentary=commentary,
                listing=listing
            )
            comment.save()
        except Exception:
            return HttpResponseRedirect(reverse('auctions:listing', args=(listing_id,)))
    return HttpResponseRedirect(reverse('auctions:listing', args=(listing_id,)))


@login_required(login_url='login')
def watchlist(request):
    user = request.user
    items = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "items": items
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def category_listing(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/category_listing.html", {
        "listings": listings
    })