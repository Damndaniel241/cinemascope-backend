from django.db import models
from users.models import User
from django.core.exceptions import ValidationError
# Create your models here.
    
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
    review = models.OneToOneField(Review,on_delete=models.CASCADE,unique=True)
    
    def __str__(self):
        return f"{self.user}'s rating on {self.movie}"
    
    
