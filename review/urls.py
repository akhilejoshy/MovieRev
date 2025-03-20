from django.urls import path
from review import views

urlpatterns = [
    path('add_review/<int:movie_id>/', views.AddReview.as_view(), name='add_review'),

    path('update/<int:movie_id>/', views.UpdateReview.as_view(), name='update_review'),  
    path('<int:movie_id>/review/delete/', views.DeleteReview.as_view(), name='delete_review'),
    path('saved-reviews/', views.Saveds.as_view(), name='saved_reviews'), 
    path('wishlist/<int:id>/', views.Wishlistview.as_view(), name='wishlist'),
    path('reviews/', views.Reviews.as_view(), name='user_reviews'), 

]
