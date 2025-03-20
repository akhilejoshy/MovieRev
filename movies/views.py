from django.shortcuts import render
from django.views import View
import requests
from datetime import date, timedelta
from user_app.forms import Loginform,User_form
from review.models import Wishlist,Review
from review.forms import ReviewForm

from review.models import Review


API_KEY = "19540a56163705856fb1501f6f63663c"
BASE_URL = "https://api.themoviedb.org/3"

class LatestMovies(View):
    def get(self, request):
        today, last_month = date.today(), date.today() - timedelta(days=30)

        english_movies = self.english_movies(today, last_month)
        malayalam_movies = self.malayalam_movies(today, last_month)
        tamil_movies = self.tamil_movies(today, last_month)
        hindi_movies = self.hindi_movies(today, last_month)

        movies = {
            "English": english_movies,
            "Malayalam": malayalam_movies,
            "Tamil": tamil_movies,
            "Hindi": hindi_movies,
        }

        return render(request, "movies/latest.html", {"latest_movies": movies})

    def english_movies(self, today, last_month):
        url = (
            f"{BASE_URL}/discover/movie?api_key={API_KEY}"
            f"&with_original_language=en"
            f"&primary_release_date.gte={last_month}"
            f"&primary_release_date.lte={today}"
            f"&sort_by=popularity.desc"
            f"&page=1"
        )
        return self.fetch_movies(url, "english_movies", today, last_month)

    def malayalam_movies(self, today, last_month):
        url = (
            f"{BASE_URL}/discover/movie?api_key={API_KEY}"
            f"&with_original_language=ml"
            f"&primary_release_date.gte={last_month}"
            f"&primary_release_date.lte={today}"
            f"&sort_by=popularity.desc"
            f"&page=1"
        )
        return self.fetch_movies(url, "malayalam_movies", today, last_month)

    def tamil_movies(self, today, last_month):
        url = (
            f"{BASE_URL}/discover/movie?api_key={API_KEY}"
            f"&with_original_language=ta"
            f"&primary_release_date.gte={last_month}"
            f"&primary_release_date.lte={today}"
            f"&sort_by=popularity.desc"
            f"&page=1"
        )
        return self.fetch_movies(url, "tamil_movies", today, last_month)

    def hindi_movies(self, today, last_month):
        url = (
            f"{BASE_URL}/discover/movie?api_key={API_KEY}"
            f"&with_original_language=hi"
            f"&primary_release_date.gte={last_month}"
            f"&primary_release_date.lte={today}"
            f"&sort_by=popularity.desc"
            f"&page=1"
        )
        return self.fetch_movies(url, "hindi_movies", today, last_month)

    def fetch_movies(self, url, movie_lang, today, last_month):
        try:
            response = requests.get(url, timeout=2)
            response.raise_for_status()
            return response.json().get("results", [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movies' '{movie_lang}: {e}")

            if movie_lang == "english_movies":
                return self.english_movies(today, last_month)
            elif movie_lang == "malayalam_movies":
                return self.malayalam_movies(today, last_month)
            elif movie_lang == "tamil_movies":
                return self.tamil_movies(today, last_month)
            elif movie_lang == "hindi_movies":
                return self.hindi_movies(today, last_month)

        

class MovieDetail(View):
    def get(self, request, movie_id):

        movie_url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits,videos"
        try:
            response = requests.get(movie_url) 
            response.raise_for_status() 
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"Error fetching movies: {e}")
            return self.get(request, movie_id) 
        movie = response.json()

        form = ReviewForm()

        count=8
        if request.user.is_authenticated:
            user_review = Review.objects.filter(user=request.user, movie_id=movie_id).first() 
            if user_review:
                user_review.solid=range(user_review.rating)
                user_review.regular=range(5-user_review.rating)
                count+=1
        else:
            user_review = None


        filter_option = request.GET.get('filter')

        reviews = Review.objects.filter(movie_id=movie_id)

        if request.user.is_authenticated:
            reviews = reviews.exclude(user=request.user) 



        if filter_option == "date":
            reviews = reviews.order_by("-created_at")  
        elif filter_option == "rating":
            reviews = reviews.order_by("-rating")

        for review in reviews:
           review.solid = range(review.rating) 
           review.regular = range(5 - review.rating)  
           count+=1

        movie_in_wishlist = Wishlist.objects.filter(user=request.user, movie_id=movie_id).exists() if request.user.is_authenticated else False

        context = {
            "form": form,
            "movie_id": movie_id,
            "title": movie.get("title", "N/A"),
            "runtime": movie.get("runtime", "N/A"),
            "release_date": movie.get("release_date", "N/A"),
            "rating": movie.get("vote_average", "N/A"),
            "cover_image": f"https://image.tmdb.org/t/p/original{movie.get('backdrop_path')}" if movie.get("backdrop_path") else None,
            "poster_image": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else None,
            "genres": [genre["name"] for genre in movie.get("genres", [])],
            "director": next((crew["name"] for crew in movie.get("credits", {}).get("crew", []) if crew["job"] == "Director"), "N/A"),
            "cast": [actor["name"] for actor in movie.get("credits", {}).get("cast", [])[:3]],  
            "summary": movie.get("overview", "No summary available."),
            "reviews": reviews,
            "user_review":user_review, 
            "count":count,
            "movie_in_wishlist": movie_in_wishlist

        }
        
        return render(request, "movies/detail.html", context)
    


class SearchMovies(View):
    def get(self, request):
        name = request.GET.get("movie", "").strip()
        movies = []

        if name:
            search_url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={name}&page=1"
            try:
                response = requests.get(search_url, timeout=5)
                response.raise_for_status()
                movies = response.json().get("results", [])[:10]
            except requests.exceptions.RequestException as e:
                print(f"Error searching movies: {e}")
                return self.get(request)


        return render(request, "movies/search.html", {"movies": movies})


