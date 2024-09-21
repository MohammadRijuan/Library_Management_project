from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from book.models import Book, Review,Category
from book.forms import ReviewForm


def HomeView(request, category_slug=None):
    books = Book.objects.all()

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(categories=category)

    categories = Category.objects.all()
    return render(request, 'index.html', {'books': books, 'categories': categories})

def About(request):
    return render(request,'About.html')
