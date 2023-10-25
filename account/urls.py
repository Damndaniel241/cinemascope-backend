from django.urls import path
# from .views import LoginView,SignupView,UpdateProfileView,LogoutView,UserProfileDetailView
from .views import *


urlpatterns = [
     path('login/', LoginView.as_view(), name='login'),
     path('signup/', SignupView.as_view(), name='signup'),
     path('update-profile/', UpdateProfileView.as_view(), name='update'),
      path('logout/', LogoutView.as_view(), name='logout'),
      path('user-profile/<str:username>/', UserProfileDetailView.as_view(), name='user-profile-detail'),
       path('user-profile/<int:id>/', UserProfileDetailViewID.as_view(), name='user-profile-detail'),
     

]




# from .views import signup,login,logout


# path('login/',login ),
# path('signup/',signup),
# path('logout/',logout),

# {"username_or_email":"ryan@goslin.com","password":"ryangoslin241"}
# {"username_or_email":"ryangoslin99","password":"ryangoslin241"}