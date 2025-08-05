from django.urls import path, include
import users.views as users_views
from .views import (
    NewLoginView, 
    NewLogoutView, 
    RegisterView, 
    UserProfileUpdateView,
    UserProfileDetailView,
    UserPasswordChangeView,      
    PasswordChangeDoneView,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)


# from . import urls as core_urls

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),  
    path("login/", NewLoginView.as_view(), name="login"),
    path("logout/", NewLogoutView.as_view(), name="logout"), 
    path('profile/<int:pk>/', UserProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/', UserProfileDetailView.as_view(), name='profile_detail'),
    path("change-password/", UserPasswordChangeView.as_view(), name="change_password"),
    path("change-password/password_changed/", PasswordChangeDoneView.as_view(), name="password_changed"),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ]