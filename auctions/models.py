from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=800)
    short = models.CharField(max_length=32, blank=True)
    bid = models.IntegerField()
    url = models.URLField(blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="listings")
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    watcher = models.ManyToManyField(User, blank=True, related_name="watchlist")
    winner = models.ForeignKey(User,blank=True, on_delete=models.CASCADE,null=True, related_name="winnings")
    

    def __str__(self):
        return f"Listing #{self.id}: {self.name} ({self.user.username})"



class Comment(models.Model):
    message = models.TextField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Comment #{self.id}: {self.user.username} on {self.listing.name}: {self.message}"


class Bid(models.Model):
    amount = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"Bid #{self.id}: {self.amount} on {self.listing.name} by {self.user.username}"