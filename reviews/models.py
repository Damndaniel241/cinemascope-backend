from django.db import models
# from django.contrib.auth import get_user_model'
from django.conf import settings




class Movie(models.Model):
    movie_id = models.CharField(max_length=15,unique=True)
    def __str__(self):
        return f"{self.movie_id}"
       

 
    # Other movie-related fields
    # ...

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # review_movie_id = models.CharField(max_length=8)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,to_field='movie_id')
 
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user}'s review for {self.movie}"
   
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} replied to {self.review.user}'s Review"
    # Other comment-related fields
    # ...

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,to_field='movie_id')
    def __str__(self):
        return f"{self.user} liked movie {self.movie}"

class Watch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    watch_date = models.DateField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,to_field='movie_id')
    def __str__(self):
        return f"{self.user} watched movie {self.movie} on {self.watch_date}"


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,to_field='movie_id')
    stars = models.PositiveIntegerField(null=True)


    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user} rated movie {self.movie}"
   


