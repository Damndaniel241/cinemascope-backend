# urls.py
from django.urls import path
# from .views import CreateReviewView
# from .views import create_review,check_like_status,like_movie,unlike_movie,rate_movie

from .views import *

urlpatterns = [
    # Other URL patterns
    path('create-review/', create_review),
    path('like/',like_movie),
    path('unlike/',unlike_movie),
    path('rate-movie/',rate_movie),
    # path('delete-rating/',delete_rating),
    path('check-like/<str:movie_id>/',check_like_status),
    path('retrieve-review/',retreive_review),
    path('reviews/<int:id>/',get_review_object),
    path('create-comment/', create_comment),
    path('comments/<int:id>/',get_comment_object),
    path('comments/review/<int:review_id>/',get_comments_for_review),
]
