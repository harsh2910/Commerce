from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create" , views.create, name="create"),
    path("listing/<int:id>", views.listing_page, name="listing_page"),
    path("listing/<int:id>?(?P<error>\d+)?/?", views.listing_page, name="listing_page"),
    path("change_watchlist/<int:id>", views.change_watchlist, name="change_watchlist"),
    path("close_listing/<int:id>", views.close_listing, name="close_listing"),
    path("bid_submit/<int:id>", views.bid_submit, name="bid_submit"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_page, name="category_page"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("winnings" , views.winnings, name="winnings"),
]