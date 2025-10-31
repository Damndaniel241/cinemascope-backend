from django.urls import path,include
from .views import signup,signin,get_by_user_name

urlpatterns =[
    path("create/", signup),
    path("login/", signin),
    path("get-user-name/",get_by_user_name),
]