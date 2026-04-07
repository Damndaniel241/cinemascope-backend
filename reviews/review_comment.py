from reviews.models import Review
from django.db import models
from users.models import User


class ReviewComment(models.Model):
    user =  models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True,related_name="reviews_commented")
    review = models.ForeignKey(Review,on_delete=models.CASCADE,related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    