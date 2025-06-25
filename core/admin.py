from django.contrib import admin

# Register your models here.
from .models import Master, Order, Service, Review

admin.site.register(Master)
admin.site.register(Order)
admin.site.register(Service)
admin.site.register(Review)