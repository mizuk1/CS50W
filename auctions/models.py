from django.contrib.auth.models import AbstractUser
from django.db import models


# represents each user of the application
class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name='watched_by')

    def __str__(self):
        return f"{self.username} ({self.email})"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_listings")
    title = models.CharField(max_length=255)
    description = models.TextField()
    current_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='listings')

    def __str__(self):
        return f"{self.owner} ({self.title}) active: {self.is_active}"
    

class Bid(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"{self.bidder.username} {self.listing.title}: {self.price}, "


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    commentary = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Commentary from: {self.user} about listing: {self.listing}"