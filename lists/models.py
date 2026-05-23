from __future__ import annotations
from django.db import models
from users.models import User
from reviews.models import Tag,Movie

from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from users.models import User
#     from reviews.models import Movie 

# Create your models here.


class List(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    title = models.CharField()
    description = models.TextField()
    tag = models.ManyToManyField(Tag,related_name="tag_lists")
    movie = models.ManyToManyField(Movie, related_name="list_movies")
    # ANYONE = "Anyone - Public List"

    def __str__(self):
        return f"{self.user.user_name}'s list -- {self.title}"



class ListLike(models.Model):
    user =  models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True,related_name="lists_liked")
    list = models.ForeignKey(List,on_delete=models.CASCADE,related_name="list_likes")

    
    def __str__(self) -> str:
        if self.user:
            return f"{self.user}'s liked {self.list.user}'s list for {self.list.movie}"
        
        else:
            return f"Deleted User liked {self.list.user}'s list for {self.list.movie}"



class ListComment(models.Model):
    user =  models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True,related_name="lists_commented")
    list = models.ForeignKey(List,on_delete=models.CASCADE,related_name="list_comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user}'s comment on {self.list.user}'s review for {self.list.movie}"
        
  
        