from .views import create_review,get_review,delete_review,update_review,rate_movie
from django.urls import path

urlpatterns=[
    path('create/',create_review),
    path('get/<int:pk>',get_review),
    path('delete/<int:pk>',delete_review),
    path('update/<int:pk>',update_review),
    path('rate/',rate_movie)
]