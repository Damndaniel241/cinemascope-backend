# from reviews.models import Review
from django.db import models
from users.models import User
from rest_framework import serializers
from users.serializers import UserProfileSerializer,UserSerializer





class ReviewLike(models.Model):
    user =  models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True,related_name="reviews_liked")
    review = models.ForeignKey('reviews.Review',on_delete=models.CASCADE,related_name="review_likes")

    
    def __str__(self) -> str:
        if self.user:
            return f"{self.user}'s liked {self.review.user}'s review for {self.review.movie}"
        
        else:
            return f"Deleted User liked {self.review.user}'s review for {self.review.movie}"
        
        
    class Meta:
        app_label = 'reviews'