from django.urls import path
from user_app import views

urlpatterns = [
    path('register/', views.Registerview.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
