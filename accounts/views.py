from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.


from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def send_email(user,subject,template):
    message = render_to_string(template,{
        'user':user
    })
    sent_email = EmailMultiAlternatives(subject,'',to=[user.email])
    sent_email.attach_alternative(message,'text/html')
    sent_email.send()




from django.views.generic import FormView
from . forms import RegForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib import messages



class UserRegistrationView(FormView):
    template_name= 'accounts/user_registration.html'
    form_class = RegForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        messages.success(self.request,'You have registered an account successfully')
        send_email(user,'Registration Message','accounts/register_email.html')

        return super().form_valid(form) #formvalid call hobe jodi  form valid hoy
    


from django.contrib.auth.views import LoginView


class UserLoginView(LoginView):
    template_name='accounts/user_login.html'
    
    def get_success_url(self):
        return reverse_lazy ('home')





from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout

class UserLogoutView(LogoutView):
    def get_success_url(self):

        if self.request.user.is_authenticated:
            logout(self.request)
            messages.success(self.request,'logged out successfully')

        return reverse_lazy('home')





from django.views import View
from . forms import UserUpdateForm
from django.shortcuts import redirect

class UserAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self,request):
        form = UserUpdateForm(instance=request.user)
        return render(request,self.template_name,{'form':form})
    

    def post(self,request):
        form = UserUpdateForm(request.POST,instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request,'Your profile has  been updated successfully')

            send_email(request.user,'Information updated Successful','accounts/update_profile_email.html')

            return redirect('home')
        
        return render(request,self.template_name,{'form':form})
    



from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView

class ChangePassView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'You have changed your password successfully')

        send_email(self.request.user,'Successfully Changed Password','accounts/change_pass_email.html')

        return super().form_valid(form)
    




