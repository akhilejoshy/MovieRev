from django.db import models
from user_app.models import User

class Review(models.Model):
    CHOICES = [
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    ]

    movie_id = models.IntegerField() 
    title = models.CharField(max_length=300)
    poster_path = models.CharField(max_length=500)  

    comment = models.TextField()  
    rating = models.PositiveIntegerField(choices=CHOICES, default='3') 
    created_at = models.DateTimeField(auto_now_add=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  

    class Meta:
        unique_together = ('user', 'movie_id') 
    
    
    



    

class Wishlist(models.Model):
    movie_id = models.IntegerField()  
    title = models.CharField(max_length=300)
    poster_path = models.CharField(max_length=500)  

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie_id') 
    
