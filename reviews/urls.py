from .views import create_review,get_review,delete_review,update_review,rate_movie,watch_movie,like_movie,add_to_watchlist,get_movie_user_data,comment_review,retreive_plat_movie_data,test_user_movie_data
from django.urls import path

urlpatterns=[
    path('create/',create_review),
    path('get/<int:pk>',get_review),
    path('delete/<int:pk>',delete_review),
    path('update/<int:pk>',update_review),
    path('rate/',rate_movie),
    path('watch/',watch_movie),
    path('like/',like_movie),
    path('add-to-watchlist/',add_to_watchlist),
    path('movie-user-data/',get_movie_user_data),
    path('comment-review/',comment_review),
    path('retrieve-plat-movie-data/',retreive_plat_movie_data),
    path('blackman/',test_user_movie_data)
]