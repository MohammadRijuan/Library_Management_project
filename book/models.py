from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=70, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    categories = models.ManyToManyField(Category)
    title = models.CharField(max_length=120)
    description = models.TextField()
    image  = models.ImageField(upload_to='book/media/uploads',blank= True, null= True)
    quantity = models.PositiveIntegerField(default = 0)
    price = models.DecimalField(max_digits=12, decimal_places=2)
   


    def __str__(self):
        return self.title

    


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class BorrowingBookHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)