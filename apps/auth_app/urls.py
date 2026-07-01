from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, MeView, UpdateProfileView, ChangePasswordView
 
urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/me/', MeView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('auth/update-profile/', UpdateProfileView.as_view()),
    path('auth/change-password/', ChangePasswordView.as_view()),
]
 