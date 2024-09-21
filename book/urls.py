from django.urls import path
from .views import borrowing_history_show,return_book,booklist_by_category,Booklist,DetailBookView,Borrowing_books
from core.views import HomeView

urlpatterns = [
    
    path('books/<slug:slug>/borrow/', Borrowing_books, name='borrow_book'),
    path('category/<slug:category_slug>/', booklist_by_category, name='booklist_by_category'),
    path('books/<int:book_id>/', Borrowing_books, name='borrow_book'),
    path('borrowing-history/', borrowing_history_show, name='borrowing_history'),
    path('borrowing-history/<int:borrowing_id>/return/', return_book, name='return_book'),
    path('book_list/', Booklist, name='book_list'),
    path('books/details/<int:pk>/', DetailBookView.as_view(), name='book_detail'),


     
]