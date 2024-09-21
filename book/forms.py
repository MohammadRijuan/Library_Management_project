from django import forms 
from . models import Book,Review

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','description','image','price','categories']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
