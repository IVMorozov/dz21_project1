from django.urls import path, include
import users.views as users_views
from .views import NewLoginView, NewLogoutView, RegisterView, UserPasswordChangeView, ProfileUser, PasswordChangeDoneView


# from . import urls as core_urls

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),  
    path("login/", NewLoginView.as_view(), name="login"),
    path("logout/", NewLogoutView.as_view(), name="logout"), 
    # path('profile/<int:pk>/', ProfileUser.as_view(), name='profile'),
    path('profile/', ProfileUser.as_view(), name='profile'),
    path("change-password/", UserPasswordChangeView.as_view(), name="change_password"),
    path("change-password/password_changed/", PasswordChangeDoneView.as_view(), name="password_changed"),
    # path('password-change/password_changed/', PasswordChangeDoneView.as_view(template_name="users/password_changed.html"), name="password_changed"),
]