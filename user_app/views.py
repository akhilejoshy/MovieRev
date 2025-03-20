from django.shortcuts import render,redirect
from django.views import View
from user_app.models import User
from user_app.forms import User_form,Loginform
from django.contrib.auth import authenticate, login, logout






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
                return render(request, 'user_app/login.html', {'form': form, 'message': message})
        return render(request, 'user_app/login.html', {'form': form})



class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('trending_movies')