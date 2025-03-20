from django import forms


class User_form(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control bg-dark text-white  border-0  py-2  rounded-pill   ','placeholder':'enter username'}))
    first_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control bg-dark text-white border-0  py-2  rounded-pill ','placeholder':'enter firstname'}))
    last_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control bg-dark text-white border-0  py-2  rounded-pill ','placeholder':'enter lastname'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control bg-dark text-white border-0  py-2  rounded-pill ','placeholder':'enter your email'}))
    password=forms.CharField(max_length=16,widget=forms.PasswordInput(attrs={'class':'form-control bg-dark text-white border-0  py-2  rounded-pill ','placeholder':'enter password'}))


class Loginform(forms.Form):
    
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control bg-dark text-white border-0 py-2  rounded-pill ','placeholder':'enter username'}))
    password=forms.CharField(max_length=16,widget=forms.PasswordInput(attrs={'class':'form-control bg-dark text-white border-0 py-2 rounded-pill ','placeholder':'enter password'}))