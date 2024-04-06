from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import json
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import *

def index(request):
    # Get all posts
    posts = Post.objects.all()

    # Get user
    try:
        user = request.user
    except Exception:
        user = None
    
    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()

    # Pagination
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    return render(request, "network/index.html", {
        "user": user,
        "posts": posts,
        "page_obj": page_obj,
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def compose(request):
    # Composing a new post must be via POST
    if request.method == "POST":
        text = request.POST['text']
        user = request.user
        post = Post(user=user,text=text)
        post.save()
        return HttpResponseRedirect(reverse('index'))
    

def profile(request, username):
    # Get profile
    profile = User.objects.get(username=username)
    # Get user
    try:
        user = request.user
    except Exception:
        user = None
    
    # POST request
    if request.method == "POST":
        profile = User.objects.get(username=username)
        try:
            follow = Follow.objects.get(follower=user, followed=profile)
        except Exception:
            follow = Follow(follower=user, followed=profile)
            follow.save()
        follow.is_active = not follow.is_active
        follow.save()
        return HttpResponseRedirect(reverse("profile", args=(profile.username,)))

    # Get all posts of this user
    posts = Post.objects.filter(user=profile)
    # Get number of followers and following of this user
    followers = profile.followers.filter(is_active=True).count()
    following = profile.following.filter(is_active=True).count()

    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()

    # Creating variable isFollowing
    isFollowing = False
    # Check if user is following the profile user
    if (user != profile):
        try:
            if (Follow.objects.get(follower=user, followed=profile).is_active):
                isFollowing = True
        except Exception:
            isFollowing = False

    # Pagination
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    return render(request, "network/profile.html", {
        "user": user,
        "posts": posts,
        "page_obj": page_obj,
        "followers": followers,
        "following": following,
        "profile": profile,
        "user": user,
        "isFollowing": isFollowing,
    })


@login_required
def following(request):
    user = request.user
    follows = Follow.objects.filter(follower=user, is_active=True)
    
    followed = []
    for follow in follows:
        followed.append(follow.followed)

    # Get all posts from followed users
    posts = Post.objects.filter(user__in=followed)
    
    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()

    # Pagination
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    return render(request, "network/following.html", {
        "user": user,
        "posts": posts,
        "page_obj": page_obj,
    })


@csrf_exempt
@login_required
def edit(request, post_id):
    if request.method == "PUT":
        user = request.user
        data = json.loads(request.body)
        # Get contents of post
        text = data.get("text")

        try:
            post = Post.objects.get(id=post_id)
            if user == post.user:
                post.text = text
                post.save()

                # Serialize post
                serialized_post = post.serialize()
                return JsonResponse(serialized_post)
            else:
                return JsonResponse({"error"})
        except Exception:
            return JsonResponse("error")
        

@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    try:
        Like.objects.get(user=user, post=post)
        liked = True
    except Exception:
        liked = False
    return JsonResponse({
        "liked": liked,
    })


@login_required
def add_like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    
    like = Like(user=user, post=post)
    like.save()

    likes = post.likes.count()
    return JsonResponse({
        "likes": likes,
    })


@login_required
def remove_like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    like = Like.objects.get(user=user, post=post)
    like.delete()
    
    likes = post.likes.count()
    return JsonResponse({
        "likes": likes,
    })
