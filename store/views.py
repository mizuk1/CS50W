from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from store import util

import json
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
def index(request):
    clients = Client.objects.all()
    categories = Category.objects.all()
    courses = Course.objects.all()
    course = Course.objects.get(pk=1)
    instructors = Instructor.objects.all()
    return render(request, "store/index.html", {
        "course": course,
        "clients": clients,
        "categories": categories,
        "courses": courses,
        "instructors": instructors,
    })


def clients(request):
    clients = Client.objects.all()
    return render(request, "store/clients.html", {
        "clients": clients,
    })


def categories(request):
    categories = Category.objects.all()
    return render(request, "store/categories.html", {
        "categories": categories,
    })


def category(request, name):
    categories = Category.objects.all()
    category = Category.objects.get(name=name)
    courses = Course.objects.filter(category=category)
    return render(request, "store/category.html", {
        "courses": courses,
        "category": category,
        "categories": categories,
    })


def course(request, course_id):
    user = request.user
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("store:login"))
    
    course = Course.objects.get(pk=course_id)
    try:
        cart = Cart.objects.get(user=user)
    except Exception:
        cart = Cart(user=user)
        cart.save()
    
    isCourseInCart = False
    for item in cart.items.all():
        if course == item.course:
            isCourseInCart = True
    
    return render(request, "store/course.html", {
        "course": course,
        "isCourseInCart": isCourseInCart,
    })


def addItem(request):
    if request.method == "POST":
        course_id = request.POST['course_id']
        user = request.user
        course = Course.objects.get(pk=course_id)
        cart = Cart.objects.get(user=user)
        item = CartItem(cart=cart, course=course)
        item.save()
        return HttpResponseRedirect(reverse("store:cart"))
    

def removeItem(request):
    if request.method == "POST":
        course_id = request.POST['course_id']
        user = request.user
        course = Course.objects.get(pk=course_id)
        cart = Cart.objects.get(user=user)
        item = CartItem.objects.get(cart=cart, course=course)
        item.delete()
        return HttpResponseRedirect(reverse("store:cart"))


def profile(request):
    user = request.user
    purchases = user.purchases.all()
    purchased_courses_list = []
    
    for purchase in purchases:
        courses_list = [course for course in purchase.courses.all()]
        purchase_dict = {
            'courses': courses_list,
            'price': purchase.total_price,
            'timestamp': purchase.timestamp
        }
        purchased_courses_list.append(purchase_dict)
    
    return render(request, "store/profile.html", {
        "user": user,
        "purchased_courses": purchased_courses_list,
    })    


def search(request):
    if request.method == "POST":
        sentence = request.POST["prompt"]
        if sentence == "":
            return HttpResponseRedirect(reverse("store:index"))
        
        courses = Course.objects.all()
        corpus = []
        for course in courses:
            corpus.append(course.name)

        courses_names = util.similar_courses(corpus, sentence)
        courses = []
        for course in courses_names:
            courses.append(Course.objects.get(name=course))

        return render(request, "store/category.html", {
        "courses": courses,
        })


def cart(request):
    user = request.user
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("store:login"))
    
    try:
        cart = Cart.objects.get(user=user)
    except Exception:
        cart = Cart(user=user)
        cart.save()

    items = cart.items.all()
    return render(request, "store/cart.html", {
        "items": items,
    })
    

def payment(request):
    if request.method == "POST":
        user = request.user
        cart = Cart.objects.get(user=user)
        cart_items = cart.items.all()
        if cart_items.count() > 0:
            new_purchase = Purchase(user=request.user)
            new_purchase.save()
            new_purchase.add_courses_from_cart(cart_items)
            for item in cart_items:
                item.delete()
    return HttpResponseRedirect(reverse("store:index"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("store:index"))
        else:
            return render(request, "store/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "store/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("store:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "store/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "store/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("store:index"))
    else:
        return render(request, "store/register.html")
