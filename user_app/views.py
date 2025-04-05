from django.shortcuts import render,redirect
from django.views import View
from user_app.models import User
from user_app.forms import User_form,Loginform
from django.contrib.auth import authenticate, login, logout



from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
import random

from user_app.models import User
from user_app.forms import *


# Helper function to send OTP
def send_otp(email, subject, otp):
    message = f"Your OTP: {otp}"
    from_mail = "akhilejoshy@gmail.com"
    send_mail(subject, message, from_mail, [email], fail_silently=True)
    print('sended')



# User Registration View
class UserRegistrView(View):
    def get(self, request):
        return render(request, 'user_app/register.html', {'form': User_form})

    def post(self, request):
        form = User_form(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data.get('username')).exists():
                return render(request, 'user_app/register.html', {
                    'form': User_form(),
                    'message': 'Username already exists. Please choose another one.'
                })
            else:
                otp = str(random.randint(1000, 9999))
                request.session['register_data'] = {'data': form.cleaned_data, 'otp': otp}
                send_otp(form.cleaned_data.get('email'), f"Hi {form.cleaned_data.get('username')}", otp)
                return redirect('verification')
        return render(request, 'user_app/register.html', {'form': form})
    


# OTP Verification View
class UserVerification(View):
    def get(self, request):
        return render(request, 'user_app/otp.html', {'form': Userverificationform})

    def post(self, request):
        form = Userverificationform(request.POST)
        data = request.session.get('register_data') or request.session.get('reset_data')
        if form.is_valid() and data :
            if form.cleaned_data.get('otp') == data['otp']:
                if 'register_data' in request.session:
                    user=User.objects.create_user(**data['data'])
                    del request.session['register_data']
                elif 'reset_data' in request.session:
                    return redirect('reset_password')
                return redirect('login')
            message='Enter valid otp'
            return render(request,'user_app/otp.html',{'form':Userverificationform(),'message':message})
    


# User Login View
class UserLoginView(View):
    def get(self, request):
        return render(request, 'user_app/login.html', {'form': Loginform})

    def post(self, request):
        form =Loginform(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user:
                login(request, user)
                return redirect('trending_movies')
            else:
                message = 'Invalid username or password'  
                return render(request, 'user_app/login.html', {'form': form, 'message': message})
        return redirect('login')
    


# Forget Password View
class ForgetPassword(View):
    def get(self, request):
        return render(request, 'user_app/forget.html', {'form': ForgetPasswordform})

    def post(self, request):
        form = ForgetPasswordform(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data.get('username'))
                otp = str(random.randint(1000, 9999))
                request.session['reset_data'] = {'username': user.username, 'otp': otp}
                send_otp(user.email, "Forgot Password OTP", otp)
                return redirect('verification')
            except User.DoesNotExist:
                message = 'Invalid username '  
                return render(request, 'user_app/forget.html', {'form': form, 'message': message})
        return redirect('forget')
    


# Reset Password View
class ResetPassword(View):
    def get(self, request):
        return render(request, 'user_app/reset_password.html', {'form': ResetForm})

    def post(self, request):
        form = ResetForm(request.POST)
        reset_data = request.session.get('reset_data')
        if reset_data and form.is_valid():
            user = User.objects.get(username=reset_data['username'])
            user.set_password(form.cleaned_data.get('new_password'))
            user.save()
            del request.session['reset_data']
            return redirect('login')
        return render(request, 'user_app/reset_password.html', {'form': form})





class Registerview(View):
    def get(self,request):
        form= User_form() 
        return render(request,'user_app/register.html',{'form':form})
    
    def post(self,request):
        form= User_form(request.POST)
        if form.is_valid():
            try:
                User.objects.create_user(**form.cleaned_data)
                return redirect('login')
            except Exception as e:
                message = 'Username already exists'
                form=User_form()  
                return render(request,'user_app/register.html',{'form':form, 'message': message})

        return render(request,'user_app/register.html',{'form':form})




class Login(View):
    def get(self, request):
        form = Loginform()  
        return render(request,'user_app/login.html',{'form': form})
    
    def post(self, request):
        form = Loginform(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            pswd = form.cleaned_data.get('password')
            user = authenticate(request, username=user_name, password=pswd)
            if user:
                login(request, user)
                return redirect('trending_movies')
            else:
                message = 'Invalid username or password'  
                print(message)
                return render(request, 'user_app/login.html', {'form': form, 'message': message})
        return render(request, 'user_app/login.html', {'form': form})



class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('trending_movies')
    



