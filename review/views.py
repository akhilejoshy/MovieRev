from django.shortcuts import redirect,render
import requests
from django.views import View
from .models import Review,Wishlist
from .forms import ReviewForm



# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# @method_decorator(login_required, name='dispatch')



API_KEY = "19540a56163705856fb1501f6f63663c"
BASE_URL = "https://api.themoviedb.org/3"


class AddReview(View):
    def post(self, request, movie_id):
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                user=request.user,
                movie_id=movie_id,
                title=request.POST.get("title"), 
                poster_path=request.POST.get("poster_path"),
                comment=form.cleaned_data["comment"],
                rating=form.cleaned_data["rating"],
            )
            return redirect("movie_detail", movie_id=movie_id)
        return redirect("movie_detail", movie_id=movie_id)  



class UpdateReview(View):
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

        rev=Review.objects.get(user=request.user,movie_id=movie_id)
        form = ReviewForm(instance=rev)
        
        count=0

        # Check for User Review
        if request.user.is_authenticated:
            user_review = Review.objects.filter(user=request.user, movie_id=movie_id).first() 
            if user_review:
                user_review.solid=range(user_review.rating)
                user_review.regular=range(5-user_review.rating)
                count+=1
        else:
            user_review = None

        # Fetch and Format Reviews from DB
        reviews = Review.objects.filter(movie_id=movie_id)
        rating=((sum(review.rating for review in reviews)*2)/(sum(1 for review in reviews) if reviews else 1))

 
        new_reviews = []
        for review in reviews:
            new_reviews.append({
                "author": review.user.username,
                "rating": review.rating,
                "content": review.comment,
                "date": review.created_at.strftime("%Y-%m-%d"),
                'solid':range(review.rating),
                'regular': range(5 - review.rating)
            })
            count += 1

        # Format TMDB Reviews        
        for tmdb_review in tmdb_reviews:
            tmdb_rating=tmdb_review.get("author_details", {}).get("rating")
            if tmdb_rating: 
                new_reviews.append({
                    "author": tmdb_review.get("author", "Anonymous"),
                    "rating": round(rating/2),
                    "content": tmdb_review.get("content", "No review content"),
                    "date": tmdb_review.get("created_at", "Unknown Date").split("T")[0] ,
                    'solid':range(round(tmdb_rating/2)),
                    'regular': range(5 - round(tmdb_rating/2))
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
            "rating": (round((rating + movie.get("vote_average", "N/A"))/(2 if rating else 1),1)),
            "cover_image": f"https://image.tmdb.org/t/p/original{movie.get('backdrop_path')}" if movie.get("backdrop_path") else None,
            "poster_image": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else None,
            "genres": [genre["name"] for genre in movie.get("genres", [])],
            "director": next((crew["name"] for crew in movie.get("credits", {}).get("crew", []) if crew["job"] == "Director"), "N/A"),
            "cast": [actor["name"] for actor in movie.get("credits", {}).get("cast", [])[:3]],
            "summary": movie.get("overview", "No summary available."),
            "reviews": new_reviews,
            "count":count,
            "movie_in_wishlist": movie_in_wishlist

        }
        
        return render(request, "movies/detail.html", context)
    


    def post(self, request, movie_id):
        review = Review.objects.filter(user=request.user, movie_id=movie_id).first()
        review.comment = request.POST.get("comment")
        review.rating = request.POST.get("rating")
        review.save()

        return redirect("movie_detail", movie_id=movie_id)


class DeleteReview(View):
    def get(self, request, movie_id):
        review = Review.objects.filter( movie_id=movie_id, user=request.user).first()
        if review:
            review.delete()
        return redirect('movie_detail', movie_id=movie_id)  
    

class Wishlistview(View):
    def post(self, request, id):        
        title = request.POST.get("title")  
        poster_path = request.POST.get("poster_path")  

        wishlist_item = Wishlist.objects.filter(user=request.user, movie_id=id).first()

        if wishlist_item:
            wishlist_item.delete()
        else:
            Wishlist.objects.create(user=request.user, movie_id=id, title=title, poster_path=poster_path)


        return redirect('movie_detail', movie_id=id) 
    



    
class Saveds(View):
    def get(self, request):
        saved_movies = Wishlist.objects.filter(user=request.user)
        count = saved_movies.count()
     
        

        context = {
            "saved_movies": saved_movies,
            "count": count,
            
        }
        return render(request, "savings/saved.html",context)
    
class Reviews(View):
    def get(self, request):
        reviews = Review.objects.filter(user=request.user)
        count = reviews.count()
        for review in reviews:
           review.solid = range(review.rating) 
           review.regular = range(5 - review.rating)
    
        

        context = {
            "reviews": reviews,
            "count": count,
        }
        return render(request,'reviews/reviews.html',context)
    






