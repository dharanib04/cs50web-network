
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("editpost", views.editPost, name="editPost"),
    path("like/<str:postid>", views.like, name="like"),
]
