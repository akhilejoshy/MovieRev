from django.urls import path
from movies import views

urlpatterns = [
    path('', views.LatestMovies.as_view(), name='trending_movies'),
    path('movie/<int:movie_id>/', views.MovieDetail.as_view(), name='movie_detail'),  
    path('search/', views.SearchMovies.as_view(), name='search_movies'),
]
