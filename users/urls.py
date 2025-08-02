from django.urls import path, include
import users.views as users_views
from .views import NewLoginView, NewLogoutView, RegisterView
from core.views import (
    OrderListView,
    )

# from . import urls as core_urls

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),  
    path("login/", NewLoginView.as_view(), name="login"),
    path("logout/", NewLogoutView.as_view(), name="logout"), 
    # path('orders/', OrderListView.as_view(), name='orders_list'),
    # path('core/', include(core_urls)),
]