from django.urls import path,include
from .views import signup,signin,get_by_user_name_or_id,test_site,activate_account,logout,token_refresh
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns =[
    path("create/", signup),
    path("login/", signin),
    path("get-user-name/",get_by_user_name_or_id),
    path('test-site/',test_site),
    path("activate/<uidb64>/<token>/",activate_account),
    path("auth/logout/",logout),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('auth/refresh',token_refresh)
    # path("try/",try_user)
    # path('verify/<uidb64>/')
]