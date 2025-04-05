from django.urls import path
from user_app.views import *

urlpatterns = [
    # path('register/', views.Registerview.as_view(), name='register'),
    # path('login/', views.Login.as_view(), name='login'),
    path('register/', UserRegistrView.as_view(), name='register'),
    path('otp/',UserVerification.as_view(),name='verification'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('forget/',ForgetPassword.as_view(),name='forget'),
    path('reset-password/', ResetPassword.as_view(), name='reset_password'),
    path('logout/',Logout.as_view(), name='logout'),

    

]

