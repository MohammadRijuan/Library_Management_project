from django.shortcuts import render,get_object_or_404
from . models import Book,Category,BorrowingBookHistory

# Create your views here.

def booklist_by_category(request, category_slug=None):
    books = Book.objects.all()
    category = None

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(categories=category)

    categories = Category.objects.all()
    return render(request, 'index.html', {'books':books, 'categories':categories, 'category':category})




from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def borrowed_books_email(user,title,subject,price,template):
    message = render_to_string(template,{
        'user':user,
        'title':title,
        'price':price
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


from accounts.models import UserAccount
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def Borrowing_books(request,book_id):
    book = get_object_or_404(Book,pk=book_id)
    account = UserAccount.objects.get(user=request.user)
    # account, created = UserAccount.objects.get_or_create(user=request.user)

    if book.quantity < 1:
        messages.error(request,'Your desired book is not available')
        return redirect('home')
    
    if book.price > account.balance :
        messages.warning(request,'Your donot have enough balance')
        return redirect('borrowing_history')
    
    book.quantity -= 1
    book.save()
    account.balance -= book.price 
    account.save(update_fields=['balance'])
    borrowing, created = BorrowingBookHistory.objects.get_or_create(user=request.user, book=book)
    if not created:
        borrowing.quantity +=1
        borrowing.save()
    
    messages.success(request, f'You have successfully borrowed {book.title} book.')
    borrowed_books_email(request.user, book.title, "Book Borrowed Successfully",book.price,"book/borrow_email.html")
    return redirect('borrowing_history')

# from django.db import IntegrityError
# from django.db import models

# @login_required
# def Borrowing_books(request, slug):
#     book = get_object_or_404(Book, slug=slug)

#     try:
#         account = UserAccount.objects.get(user=request.user)
#     except UserAccount.DoesNotExist:
#         # Generate a unique account number
#         max_account_no = UserAccount.objects.aggregate(models.Max('account_no'))['account_no__max']
#         new_account_no = max_account_no + 1 if max_account_no is not None else 1  # Start from 1 if no accounts exist

#         account = UserAccount.objects.create(
#             user=request.user,
#             account_no=new_account_no,
#             account_type='default_type',  # Set a default or get from the request
#             balance=0,  # Initial balance
#         )

#     if book.quantity < 1:
#         messages.error(request, 'Your desired book is not available')
#         return redirect('book_list')  # Change this to a valid URL name

#     if book.price > account.balance:
#         messages.error(request, 'You do not have enough balance')
#         return redirect('book_list')  # Change this to a valid URL name

#     book.quantity -= 1
#     book.save()
#     account.balance -= book.price
#     account.save(update_fields=['balance'])
    
#     borrowing, created = BorrowingBookHistory.objects.get_or_create(user=request.user, book=book)
#     if not created:
#         borrowing.quantity += 1
#         borrowing.save()

#     messages.success(request, f'You have successfully borrowed {book.title} book.')
#     # Assuming borrowed_books_email is defined elsewhere
#     # borrowed_books_email(request.user, book.title, book.price, "Book Borrowed Successfully", "transactions/borrow_email.html")
    
#     return redirect('borrowing_history')  # Ensure this is a valid URL name



@login_required
def return_book(request, borrowing_id):
    borrowing = get_object_or_404(BorrowingBookHistory, pk=borrowing_id)
    user_account = UserAccount.objects.get(user=request.user)
    user_account.balance += borrowing.book.price
    user_account.save()
    borrowing.book.quantity += 1
    borrowing.book.save()
    borrowing.quantity -=1
    if borrowing.quantity<1:
        borrowing.delete()
        messages.warning(request, 'Book returned and borrowing history deleted because quantity became zero.')
    else:
        borrowing.save()
        messages.success(request, 'Book returned successfully.')
    borrowed_books_email(request.user,borrowing.book.title,"Book Returned Successfully", borrowing.book.price, "book/return_email.html")
    return redirect('borrowing_history')


@login_required
def borrowing_history_show(request):
    borrowings = BorrowingBookHistory.objects.filter(user= request.user).order_by('-borrow_date')
    for borrowing in borrowings:
        borrowing.total_price_cur = borrowing.book.price * borrowing.quantity
    total_price = sum(borrowing.book.price * borrowing.quantity for borrowing in borrowings)
    return render(request,'book/borrowing_history.html',{'borrowings':borrowings ,'total_price':total_price})


from .models import Book, Review,Category
from .forms import ReviewForm
from django.views.generic import DetailView

class DetailBookView(DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    form_class = ReviewForm

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        comment_form = self.form_class(data=request.POST)

        user_has_borrowed = BorrowingBookHistory.objects.filter(user=request.user, book=book).exists()
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.user = request.user  # request.user user instance hisebe teke jabe
            new_comment.save()
             
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = Review.objects.filter(book=book)
        # reviews=book.reviews.all()
        comment_form = self.form_class()

        if self.request.user.is_authenticated:
            user_has_borrowed = BorrowingBookHistory.objects.filter(user=self.request.user, book=book).exists()
        else:
            user_has_borrowed = False

        context['reviews'] = reviews
        context['comment_form'] = comment_form
        context['user_has_borrowed'] = user_has_borrowed
        return context
    

def Booklist(request, category_slug=None):
    books = Book.objects.all()

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(categories=category)

    categories = Category.objects.all()
    return render(request, 'book/book_list.html', {'books': books, 'categories': categories})

