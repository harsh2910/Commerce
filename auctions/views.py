from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(status=True)
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

def create(request):
    if request.method == "POST":
        listing = Listing()
        listing.name = request.POST.get("title")
        listing.description = request.POST.get("description")
        short = str(listing.description)
        if len(short) <= 32:
            listing.short = short
        else:
            short = short[0:29] + "..."
            listing.short = short
        if request.POST.get("category") != "Select":
            listing.category = Category.objects.get(id=int(request.POST.get("category")))
        listing.bid = request.POST.get("bid")
        if request.POST.get("link"):
            listing.url = request.POST.get("link")
        else:
            listing.url ="https://www.translationvalley.com/wp-content/uploads/2020/03/no-iamge-placeholder.jpg"
        listing.user = request.user
        listing.save()
        return redirect('index')
    
    else:
        return render(request, "auctions/create.html", {
            "categories": Category.objects.all()
        })

def listing_page(request, id, error=None):
    try:
        listing = Listing.objects.get(id=id)
    except:
        return redirect('index')
    try:
        comments = Comment.objects.filter(listing=listing)
    except:
        comments = None
    added = False
    owner = False
    try:
        bidder = Bid.objects.get(listing=listing, amount=listing.bid)
    except:
        bidder = None
    if request.user.username:
        try:
            if Listing.objects.get(id=id) in request.user.watchlist.all():
                added = True
        except:
            added = False

        try:
            if Listing.objects.get(id=id) in request.user.listings.all():
                owner = True
        except:
            owner = False
    else:
        added = False
        owner = False

    
    return render(request, "auctions/listing.html", {
        "listing":listing,
        "comments":comments,
        "added":added,
        "owner":owner,
        "error":error,
        "bidder":bidder,
    })

def change_watchlist(request, id):
    if request.user.username:
        listing = Listing.objects.get(id=id)
        watchlist = request.user.watchlist
        if listing in watchlist.all():
            watchlist.remove(listing)
        else:
            watchlist.add(listing)

        return redirect('listing_page', id=id)
    else:
        return redirect('index')

def close_listing(request, id):
    if request.user:
        if Listing.objects.get(id=id) in request.user.listings.all():
            listing = Listing.objects.get(id=id)
            listing.status = False
            try:
                winner = Bid.objects.get(listing=listing, amount=listing.bid)
            except:
                winner = listing
            listing.winner = winner.user
            listing.save()
            return redirect('index')
        else:
            return redirect('listing_page', id=id)
    else:
        return redirect('index')

def bid_submit(request, id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=id)
        bidder = Bid()
        current_bid = int(listing.bid)
        new_bid = int(request.POST.get('bid'))
        if new_bid > current_bid:
            listing.bid = new_bid
            listing.save()
            bidder.amount = new_bid
            bidder.user = request.user
            bidder.listing = listing
            bidder.save()
            
            return redirect('listing_page', id=id)

        else:
            error = "Bid should be greater than current bid"
            return redirect('listing_page', id=id, error=error)
    else:
        return redirect('index')



def comment(request, id):
    if request.method == "POST":
        comment = Comment()
        comment.listing = Listing.objects.get(id=id)
        comment.message = request.POST.get('comment')
        comment.user = request.user
        comment.save()
        return redirect('listing_page', id=id)
    else:
        return redirect('index')

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories":Category.objects.all()
    })

def category_page(request, category):
    category = Category.objects.get(id=category)
    return render(request, "auctions/index.html", {
        "listings": category.listings.filter(status = True)
    })

def watchlist(request):
    if request.user:
        user = request.user
        return render(request, "auctions/watchlist.html", {
        "listings": user.watchlist.filter(status = True)
        })
        

def winnings(request):
    if request.user:
        user = request.user
        listings = user.winnings.all()
        
        return render(request, "auctions/winnings.html", {
            "listings":listings
        })
    else:
        return redirect('index')

