from django.urls import path, include
from .views import (
    signup,
    signin,
    get_by_user_name_or_id,
    test_site,
    activate_account,
    logout,
    token_refresh,
    change_password,
    forgot_password,
    verify_reset_passsword_token,
    reset_password,
    follow_user,
)
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path("create/", signup),
    path("login/", signin),
    path("get-user-name/", get_by_user_name_or_id),
    path("test-site/", test_site),
    path("activate/", activate_account),
    path("auth/logout/", logout),
    path("api/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("auth/refresh", token_refresh),
    path("change-password/", change_password),
    path("password/forgot/", forgot_password),
    path('reset_confirm/',verify_reset_passsword_token),
    path("password/reset/",reset_password),
    path("follow_user/",follow_user)
    # path('verify/<uidb64>/')
]
