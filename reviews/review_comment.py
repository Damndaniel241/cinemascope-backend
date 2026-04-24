# from reviews.models import Review
from django.db import models
from users.models import User
from rest_framework import serializers
from users.serializers import UserProfileSerializer,UserSerializer


class ReviewComment(models.Model):
    user =  models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True,related_name="reviews_commented")
    review = models.ForeignKey('reviews.Review',on_delete=models.CASCADE,related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user}'s comment on {self.review.user}'s review for {self.review.movie}"
        
    class Meta:
        app_label = 'reviews'
        

