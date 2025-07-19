from django.urls import path
import users.views as users_views

urlpatterns = [
    path('register/', users_views.register_view, name='register' ),  
    path('login/', users_views.login_view, name='login'),  
    path('logout/', users_views.logout_view, name='logout'),  
]