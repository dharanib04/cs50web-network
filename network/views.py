from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

from .models import User, Post, Likes, Followers


def index(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = request.user
        if content != "":
            data = Post(user=user, content=content)
            data.save()
    post_list = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": page_obj,
        "user": request.user,
        "AllPost": True
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

def profile(request, username):
    if (request.user.is_authenticated):
            user = User.objects.get(username=username)
            post_list = Post.objects.filter(user=user).order_by("-timestamp")
            paginator = Paginator(post_list, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, "network/profile.html", {
        "user": user,
        "current_user": request.user,
        "posts": page_obj,
        "following": user.followingUsers.all().count(),
        "followers": user.beingFollowed.all().count(),
        "is_following": Followers.objects.filter(user=request.user, following=user).exists()   
    })
    else:
        return HttpResponseRedirect(reverse("login"))
    
@csrf_exempt
def follow(request, username):
    user = request.user
    if request.method == "PUT":
        following = User.objects.get(username=username)
        alrExist = Followers.objects.filter(user=user, following=following).exists()
        if not alrExist:
            data = Followers(user=user, following=following)
            data.save()
        return JsonResponse({
            "message": "Successfully followed user",
        }, status=200)
    return JsonResponse({
        "message": "Failed to follow user",
    }, status=400)

@csrf_exempt
def unfollow(request, username):
    if request.method == "PUT":
        username_id = User.objects.get(username=username).id
        user_id = User.objects.get(username=request.user).id
        data = Followers.objects.get(user=user_id, following=username_id)
        if data:
            data.delete()
        return JsonResponse({
            "message": "Successfully unfollowed user",
        }, status=200)
    return JsonResponse({
        "message": "Failed to unfollow user",
    }, status=400)
    
def following(request):
    if request.user.is_authenticated:
        user = request.user
        following = Followers.objects.filter(user=user).values_list('following', flat=True)
        userId = User.objects.filter(id__in=following)
        allpost = Post.objects.filter(user__in=userId).order_by("-timestamp")
        paginator = Paginator(allpost, 10) # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "posts": page_obj,
            "user": request.user,
            "AllPost": False
        })
    else:
        return HttpResponseRedirect(reverse("login"))
    
def listing(request):
    contact_list = Post.objects.all()
    paginator = Paginator(contact_list, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sample.html', {'page_obj': page_obj})
    
@csrf_exempt
def editPost(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        post = Post.objects.get(id=data.get("id"))
        content = data.get("content")
        post.content = content
        post.save()
        return JsonResponse({
            "message": "Successfully edited post",
        }, status=200)
    return JsonResponse({
        "message": "Failed to edit post",
        }, status=400)

@csrf_exempt
@login_required
def like(request, postid):   
    post = Post.objects.get(id=postid)
    user_id = User.objects.get(username=request.user).id
    if request.method == "PUT":
       if json.loads(request.body).get("like"):
           data = Likes(user=User.objects.get(username=request.user), post=post)
           post.likes_count = post.likes_count + 1
           post.save()
           data.save()
       else:
           data = Likes.objects.get(user=user_id, post=postid)
           post.likes_count = post.likes_count - 1
           post.save()
           data.delete()
    liked = Likes.objects.filter(user=user_id, post=postid).exists()
    return JsonResponse({"liked": liked})