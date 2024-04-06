from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

from django import forms

class ListingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-group', 
        'placeholder': 'Title'
    }))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class': 'form-control form-group', 
        'placeholder': 'Price', 
        'step': '0.01'
    }))
    imageUrl = forms.URLField(widget=forms.URLInput(attrs={
        'class': 'form-control form-group', 
        'placeholder': 'Image URL'
    }), required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control form-group'
    }), empty_label="Category")
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control form-group', 
        'placeholder': 'Description'
    }))


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control form-group', 
        'placeholder': 'Comment'
    }))

class BidForm(forms.Form):
    bid = forms.DecimalField(widget=forms.NumberInput(attrs={
        'class': 'form-control form-group', 
        'placeholder': 'Price', 
        'step': '0.01'
    }))


def index(request):
    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ListingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            title = form.cleaned_data['title']
            price = form.cleaned_data['price']
            imageUrl = form.cleaned_data['imageUrl']
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']

            newListing = Listing(
                owner=request.user,
                title=title,
                price=price,
                image_url=imageUrl,
                category=category,
                description=description,
            )
            newListing.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse("index"))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ListingForm()

    return render(request, 'auctions/create.html', {
        'form': form
    })


def listing(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            comment = form.cleaned_data['comment']
            newComment = Comment(
                user=user,
                listing=listing,
                comment=comment,
            )
            newComment.save()
        # redirect to a new URL:
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm()
        bidForm = BidForm()

    watching = False
    if user in listing.watchlist.all():
        watching = True

    comments = listing.comments.all()
    isOwner = user.username == listing.owner.username
    try:
        winnerBid = listing.bids.get(price=listing.price)
    except Exception:
        winnerBid = None
    if listing.is_active:
        winnerBid = None

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watching": watching,
        "comments": comments,
        "form": form,
        "bidForm": bidForm,
        "isOwner": isOwner,
        "winnerBid": winnerBid,
        "user": user,
    })


def unwatch(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))


def watch(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))


def close(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.is_active = False
    listing.save()
    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))


def bid(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BidForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            bid = form.cleaned_data['bid']
            if bid > listing.price:
                newBid = Bid(
                    bidder=user,
                    listing=listing,
                    price=bid,
                )
                listing.price = bid
                listing.save()
                newBid.save()
            else:
                error = "Bid must be greater than the actual price."
                form = CommentForm()
                bidForm = BidForm()

                watching = False
                if user in listing.watchlist.all():
                    watching = True

                comments = listing.comments.all()
                isOwner = user.username == listing.owner.username
                try:
                    winnerBid = listing.bids.get(price=listing.price)
                except Exception:
                    winnerBid = None
                if listing.is_active:
                    winnerBid = None
                return render(request, "auctions/listing.html", {
                    "message": error,
                    "listing": listing,
                    "watching": watching,
                    "comments": comments,
                    "form": form,
                    "bidForm": bidForm,
                    "isOwner": isOwner,
                    "winnerBid": winnerBid,
                    "user": user,
                })
        # redirect to a new URL:
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def watchlist(request):
    user = request.user
    listings = user.watching.all()

    return render(request, "auctions/watchlist.html", {
        "listings": listings,
    })


def categories(request):
    if request.method == "POST":
        categoryName = request.POST["category"]
        category = Category.objects.get(name=categoryName)
        listings = Listing.objects.filter(category=category)
        return render(request, "auctions/category.html", {
            "listings": listings,
            "category": category,
        })
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
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
