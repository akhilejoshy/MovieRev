from django import forms


class User_form(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control bg-secondary text-white  border-0  py-2     ','placeholder':'enter username'}))
    first_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control bg-secondary text-white border-0  py-2   ','placeholder':'enter firstname'}))
    last_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control bg-secondary text-white border-0  py-2   ','placeholder':'enter lastname'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control bg-secondary text-white border-0  py-2   ','placeholder':'enter your email'}))
    password=forms.CharField(max_length=16,widget=forms.PasswordInput(attrs={'class':'form-control bg-secondary text-white border-0  py-2   ','placeholder':'enter password'}))


class Loginform(forms.Form):
    
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control bg-secondary text-white border-0 py-2  ','placeholder':'enter username'}))
    password=forms.CharField(max_length=16,widget=forms.PasswordInput(attrs={'class':'form-control bg-secondary text-white border-0 py-2  ','placeholder':'enter password'}))



 
class Userverificationform(forms.Form):
    otp=forms.CharField(max_length=4,widget=forms.TextInput(attrs={'class':'form-control bg-secondary text-white border-0 py-2   ','placeholder':'enter username'}))


class ForgetPasswordform(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control bg-secondary text-white border-0 py-2   ','placeholder':'enter username'}))



class ResetForm(forms.Form):
    new_password =forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control bg-secondary text-white border-0 py-2   ','placeholder':'New Password'}))
