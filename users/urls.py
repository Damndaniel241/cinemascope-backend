from django.urls import path,include
from .views import signup,signin,get_by_user_name,test_site,activate_account

urlpatterns =[
    path("create/", signup),
    path("login/", signin),
    path("get-user-name/",get_by_user_name),
    path('test-site/',test_site),
    path("activate/<uidb64>/<token>/",activate_account)
    # path('verify/<uidb64>/')
]