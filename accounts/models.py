from django.db import models
from django.contrib.auth.models import User
from . constants import GENDER,ACCOUNT_TYPE

# Create your models here.

class UserAccount(models.Model):
    user = models.OneToOneField(User,related_name='account',on_delete=models.CASCADE)
    
    account_type = models.CharField( max_length=10,choices=ACCOUNT_TYPE)

    account_no = models.IntegerField(unique=True) # account no unique hobe...karo sathe same hobena
    birth_date = models.DateField(null=True,blank=True)

    gender = models.CharField(max_length=10,choices=GENDER)

    initial_deposit_date = models.DateField(auto_now_add=True)

    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2) # 1jn user er 12digit obdi tk rakte parbe ...r 2dhosomik obdi rakte parbe - 1000.50 eirkm...1000.50528 na
    

    def __str__(self):
          return str(self.account_no)
    

class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=120)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=100)
    
    def __str__(self):
         return self.user.username
