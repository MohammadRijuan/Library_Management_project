from django import forms
from . models import Transaction,UserAccount

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount','transaction_type']


    def __init__(self,*args,**kwargs):
        self.account = kwargs.pop('account')  #account take ber kore niye asbo..mane capture korrlam
        super().__init__(*args,**kwargs)

        self.fields['transaction_type'].disabled = True # ei field disable thakbe r user teke hide kora thakbe
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self,commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance 

        return super().save()
    

class DepositForm(TransactionForm):
    def clean_amount(self): #amount field ke filter korbo...r j field ke use kora lagbe sey field ke clean add kore cll korbo..jmn clean_balance
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount') # user er fillup kora form teke amra amount  field er value ke niye aslam 

        if amount < min_deposit_amount :
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount}$'
            )
        return amount
