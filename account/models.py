from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from .custom import CustomUserManager
from reviews.models import Review,Comment,Movie
# Create your models here.


# from django.contrib.auth.models import User
from django.conf import settings

# accounts/models.py

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    

class WatchList(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,to_field='movie_id')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following', blank=True)
    user_reviews = models.ManyToManyField(Review, related_name='reviewed_by', blank=True)
    user_comments = models.ManyToManyField(Comment, related_name='commented_by', blank=True)
    liked_reviews = models.ManyToManyField(Review, related_name='liked_by', blank=True)
    rated_reviews = models.ManyToManyField(Review, related_name='rated_by', blank=True)
    liked_movies = models.ManyToManyField(Movie, related_name='liked_by', blank=True)
    rated_movies = models.ManyToManyField(Movie, related_name='rated_by', blank=True)
    # watchlist = models.OneToOneField(WatchList,on_delete=models.CASCADE,to_field="movie")

    def __str__(self):
        return f"{self.user.username}'s profile"
