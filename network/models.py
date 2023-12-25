from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

    def __str__(self):
        return self.username


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    likes_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

class Likes(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Followers(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followingUsers")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="beingFollowed")

    def __str__(self):
        return self.user.username + " " + "is following" + " " + self.following.username