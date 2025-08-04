"""
URL configuration for barbershop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import (
    LandingView, 
    ThanksTemplateView, 
    OrderDetailView,   
    OrderListView,
    MastersListView, 
    services_list, 
    AboutTemplateView, 
    reviews, 
    OrderCreateView, 
    ReviewCreateView,
    get_master_services
    )

from django.conf import settings
from django.conf.urls.static import static
from users import urls as users_urls

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', LandingView.as_view(), name='landing'),    
    path('thanks/', ThanksTemplateView.as_view(), name='thanks'),
    path('orders/', OrderListView.as_view(), name='orders_list'),

    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('masters/', MastersListView.as_view(), name='masters_list'),
    path('services/', services_list, name='services_list'),
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('reviews/', reviews, name='reviews'),
    path('make_appointment/', OrderCreateView.as_view(), name='make_appointment'),
    path("reviews/create/", ReviewCreateView.as_view(), name="review_create"),
    path('ajax/get-master-services/', get_master_services, name='get_master_services'),
    path('users/', include(users_urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
