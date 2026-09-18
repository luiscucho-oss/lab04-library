from django.contrib import admin
from .models import Category, Publisher, Author, AuthorProfile, Book

admin.site.register(Category)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(AuthorProfile)
admin.site.register(Book)
