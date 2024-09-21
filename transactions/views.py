from django.db.models.query import QuerySet
from django.shortcuts import render,redirect

# Create your views here.

#email er jonno
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_transaction_email(user,amount,subject,template):
    message = render_to_string(template, {
        'user':user,
        'amount':amount,
    })
    send_email = EmailMultiAlternatives(subject,'',to=[user.email])
    send_email.attach_alternative(message,'text/html')
    send_email.send()


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from . models import Transaction
from django.urls import reverse_lazy

class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transaction_report')
    
    def get_form_kwargs(self): #ata amdr data pass korbe amdr form ke
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account' : self.request.user.account,
        })
        return kwargs
    
    def get_context_data(self, **kwargs):  # amdr front end ke show korbe
        context = super().get_context_data(**kwargs)
        context.update({
            'title' : self.title
        })
        return context



from . forms import DepositForm
from django.contrib import messages
from .constants import DEPOSIT


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount # amount = 200, tar ager balance = 0 taka new balance = 0+200 = 200
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )

        send_transaction_email(self.request.user,amount,"Deposite Message","transactions/deposit_email.html")
        return super().form_valid(form)

from accounts.models import UserAccount
from django.views import View

# class DepositMoneyView(View):
#     template_name = 'transactions/transaction_form.html'

#     def get(self, request):
#         try:
#             account = request.user.account
#         except UserAccount.DoesNotExist:
#             messages.error(request, "You do not have an account. Please create an account before making a deposit.")
#             return redirect('profile')
#         return render(request, self.template_name, {'account': account})

    

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from datetime import datetime
from django.db.models import Sum

class TransactionReportView(LoginRequiredMixin,ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    balance = 0

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account = self.request.user.account
        )
        #string akare nilam
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            #date e convert korlam
            start_date  = datetime.strptime(start_date_str,"%Y-%M-%d").date()
            end_date  = datetime.strptime(start_date_str,"%Y-%M-%d").date()
            
            queryset = queryset.filter(timestamp__date__gte = start_date, timestamp__date__lte =end_date)
            
            
            self.balance = Transaction.objects.filter(timestamp__date__gte = start_date , timestamp__date__lte = end_date).aggregate(Sum('amount'))
            ['amount_sum']

        else:
            self.balance = self.request.user.account.balance

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account':self.request.user.account

        })
        return context

    