from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{ self.title }"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_price = models.IntegerField()
    image = models.URLField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="categorylist")
    active = models.BooleanField()

    def __str__(self):
        return f"{ self.title }"

class Comments(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING, related_name="listing_comments")

    def __str__(self):
        return f"{self.listing.title} - {self.user.username} - {self.text}"

class Bids(models.Model):
    value = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING, related_name="bids_history")

    def __str__(self):
        return f"{self.listing.title} - {self.user.username} - {self.value}"


