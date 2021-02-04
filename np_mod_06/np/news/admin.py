from django.contrib import admin
#from django.contrib.auth.models import User
from .models import Author, Category, Post, PostCategory, Comment

#admin.site.register(User)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
