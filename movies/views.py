from django.shortcuts import render
from django.views import View
import requests
from datetime import date, timedelta
from review.models import Wishlist,Review
from review.forms import ReviewForm



API_KEY = "19540a56163705856fb1501f6f63663c"
BASE_URL = "https://api.themoviedb.org/3"

class LatestMovies(View):
    def get(self, request):
        today=date.today()
        last_month=date.today() - timedelta(days=30)

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

        # Get Movie Details
        movie_url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits,videos"
        try:
            response = requests.get(movie_url)
            response.raise_for_status()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"Error fetching movies: {e}")
            return self.get(request, movie_id)
        movie = response.json()

        # Get TMDB Reviews
        reviews_url = f"{BASE_URL}/movie/{movie_id}/reviews?api_key={API_KEY}"
        try:
            reviews_response = requests.get(reviews_url)
            reviews_response.raise_for_status()
            tmdb_reviews = reviews_response.json().get("results", [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching TMDB reviews: {e}")
            return self.get(request, movie_id)

        form = ReviewForm()

        count = 0

        # Check for User Review

        if request.user.is_authenticated:
            user_review = Review.objects.filter(user=request.user, movie_id=movie_id).first()
            if user_review:
                user_review.solid = range(user_review.rating)
                user_review.regular = range(5 - user_review.rating)
                count += 1
        else:
            user_review = None

        # Fetch and Format Reviews from DB
        reviews = Review.objects.filter(movie_id=movie_id)
        rating = ((sum(review.rating for review in reviews) * 2) / (sum(1 for review in reviews) if reviews else 1))

        new_reviews = []
        for review in reviews:
            new_reviews.append({
                "author": review.user.username,
                "rating": review.rating,
                "content": review.comment,
                "date": review.created_at.strftime("%Y-%m-%d"),
                "solid": range(review.rating),
                "regular": range(5 - review.rating)
            })
            count += 1

        # Format TMDB Reviews
        for tmdb_review in tmdb_reviews:
            tmdb_rating = tmdb_review.get("author_details", {}).get("rating")
            if tmdb_rating:
                new_reviews.append({
                    "author": tmdb_review.get("author", "Anonymous"),
                    "rating": round(tmdb_rating / 2),
                    "content": tmdb_review.get("content", "No review content"),
                    "date": tmdb_review.get("created_at", "Unknown Date").split("T")[0],
                    "solid": range(round(tmdb_rating / 2)),
                    "regular": range(5 - round(tmdb_rating / 2))
                })
                count += 1
        

        # Sort Reviews
        filter_option = request.GET.get('filter')
        if filter_option == "date":
            new_reviews.sort(key=lambda x: x["date"], reverse=True)
        elif filter_option == "rating":
            new_reviews.sort(key=lambda x: x["rating"], reverse=True)
            

        # Wishlist Check
        movie_in_wishlist = Wishlist.objects.filter(user=request.user, movie_id=movie_id).exists() if request.user.is_authenticated else False

        context = {
            "form": form,
            "movie_id": movie_id,
            "title": movie.get("title", "N/A"),
            "runtime": movie.get("runtime", "N/A"),
            "release_date": movie.get("release_date", "N/A"),
            "rating": round((rating + movie.get("vote_average", "N/A")) / (2 if rating else 1), 1),
            "cover_image": f"https://image.tmdb.org/t/p/original{movie.get('backdrop_path')}" if movie.get("backdrop_path") else None,
            "poster_image": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else None,
            "genres": [genre["name"] for genre in movie.get("genres", [])],
            "director": next((crew["name"] for crew in movie.get("credits", {}).get("crew", []) if crew["job"] == "Director"), "N/A"),
            "cast": [actor["name"] for actor in movie.get("credits", {}).get("cast", [])[:3]],
            "summary": movie.get("overview", "No summary available."),
            "reviews": new_reviews,
            "user_review": user_review,
            "count": count,
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
                response = requests.get(search_url)
                response.raise_for_status()
                movies = response.json().get("results", [])[:24]
            except requests.exceptions.RequestException as e:
                print(f"Error searching movies: {e}")
                return self.get(request)


        return render(request, "movies/search.html", {"movies": movies})


