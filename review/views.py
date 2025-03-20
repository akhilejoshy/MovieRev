from django.shortcuts import redirect,render
import requests
from django.views import View
from .models import Review,Wishlist
from .forms import ReviewForm
from user_app.forms import User_form,Loginform



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

        movie_url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits,videos"
        try:
            response = requests.get(movie_url) 
            response.raise_for_status() 
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"Error fetching movies: {e}")
            return self.get(request, movie_id) 
        movie = response.json()

        rev=Review.objects.get(user=request.user,movie_id=movie_id)
        form = ReviewForm(instance=rev)
        
        count=8
        if request.user.is_authenticated:
            user_review = Review.objects.filter(user=request.user, movie_id=movie_id).first() 
            if user_review:
                user_review.solid=range(user_review.rating)
                user_review.regular=range(5-user_review.rating)
                count+=1
        else:
            user_review = None

        reviews = Review.objects.filter(movie_id=movie_id)
        if request.user.is_authenticated:
            reviews = reviews.exclude(user=request.user) 
        reviews = reviews.order_by('-created_at')       

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
    






