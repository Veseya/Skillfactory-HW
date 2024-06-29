from .models import Category, Response, Post, User

from django.contrib import admin

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Response)