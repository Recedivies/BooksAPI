from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from authorization.views import (
    RegisterView,
    ChangePasswordView,
    UpdateProfileView,
    LogoutView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('password/<int:pk>/', ChangePasswordView.as_view(), name='change_password'),
    path('profile/<int:pk>/', UpdateProfileView.as_view(), name='update_profile'),
    path('logout/', LogoutView.as_view(), name='logout')
]
