from django.urls import path
from .views import CustomerRegistrationAPIView, StaffRegistrationAPIView, UserDeleteView, UserUpdateView, activate_user
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.authtoken.views import obtain_auth_token
from .views import LogoutView

urlpatterns = [
    path('register/customer/', CustomerRegistrationAPIView.as_view(), name='customer-registration'),
    path('register/staff/', StaffRegistrationAPIView.as_view(), name='staff-registration'),
    path('Login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtain JWT token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Verify JWT token
    path('token/obtain/', obtain_auth_token, name='auth_token_obtain'),  # Obtain Token authentication token
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/', activate_user, name='activate_user'),
    path('delete/', UserDeleteView.as_view(), name='user_delete'),
    path('update/', UserUpdateView.as_view(), name='user_update'),
]
