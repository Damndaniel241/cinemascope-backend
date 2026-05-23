from django.urls import path
from .views import create_list

urlpatterns = [
    path("create/",create_list)
    ]