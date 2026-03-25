from django.db import models
from users.models import User
from django.core.exceptions import ValidationError
# Create your models here.
from django.db.models import UniqueConstraint
    
def get_deleted_user():
    return User.objects.get_or_create(username='deleted_user')[0]

class Movie(models.Model):
    movie_id = models.CharField(max_length=20)
    
    # def add_review(self):
    def __str__(self):
        return self.movie_id

    # @property
    # def ratings(self):
        


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.SET(get_deleted_user),related_name="movie_reviews")
    content = models.TextField()
    # watched = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return f"{self.user}'s review of {self.movie}"
    
    
def validate_star_length(value):
    if value > 5:
        raise ValidationError("value is greater than 5")
    return value
    
    
class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.SET(get_deleted_user),related_name="movie_ratings")
    stars = models.PositiveIntegerField(validators=[validate_star_length])
    # review = models.OneToOneField(Review,on_delete=models.CASCADE,unique=True)
    
    def __str__(self):
        return f"{self.user}'s rating on {self.movie}"
    
    class Meta:
        constraints = [UniqueConstraint(fields=['movie','user'], name="unique_user_movie_rating")]
    
    
class Watch(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,related_name="watched")
    user = models.ForeignKey(User, on_delete=models.SET(get_deleted_user),related_name="movies_watched")
    date_watched = models.DateField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self):
        return f"{self.user.user_name} watched {self.movie} on {self.date_watched}"
    
   
    class Meta:
        constraints = [UniqueConstraint(fields=['movie','user'], name="unique_user_movie_watch")]
    
class Like(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,related_name="likes")
    user = models.ForeignKey(User, on_delete=models.SET(get_deleted_user),related_name="movies_liked")
    # liked = models.BooleanField(default=False)
    
    
    
    def __str__(self):
        return f"{self.user.user_name} liked {self.movie}"
    
    class Meta:
        constraints = [UniqueConstraint(fields=['movie','user'], name="unique_user_movie_like")] # replacement for unique_together
    
 

class WatchList(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,related_name="watch_listed")
    user = models.ForeignKey(User, on_delete=models.SET(get_deleted_user),related_name="movies_watchlisted")
    # added = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.user_name} watched {self.movie}"
    
    
    class Meta:
        constraints = [UniqueConstraint(fields=['movie','user'], name="unique_user_movie_watchlist")]