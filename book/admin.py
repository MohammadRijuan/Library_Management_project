from django.contrib import admin
from .models import Category, Book, Review, BorrowingBookHistory

# Register your models here.

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(BorrowingBookHistory)