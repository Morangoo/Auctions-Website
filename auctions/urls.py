from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("categories", views.category_list, name="categories"),
    path("<int:categoryid>/listings", views.category_listings, name="category_listings"),
    path("createlisting", views.create_listing, name="createlisting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("closedlistings", views.closed_listings, name="closedlistings"),
    path("wonlistings", views.won_listings, name="wonlistings")
]
