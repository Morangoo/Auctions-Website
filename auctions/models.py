from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"
    
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{ self.title }"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="list_category")

    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)

    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_wins", null=True, blank=True)

    active = models.BooleanField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")

    def __str__(self):
        return f"{ self.title }"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    content = models.CharField(max_length=255)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")

    def __str__(self):
        return f"{ self.content }"


class Bid(models.Model):
    value = models.DecimalField(max_digits=10 ,decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")

    def __str__(self):
        return f"{ self.value }"
