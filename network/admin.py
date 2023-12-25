from django.contrib import admin

# Register your models here.
from .models import Post, User, Followers, Likes

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Followers)
admin.site.register(Likes)
