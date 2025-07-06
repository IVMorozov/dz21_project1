from django.contrib import admin
from django.db.models import Count

# Register your models here.
from .models import Master, Order, Service, Review

admin.site.register(Master)
admin.site.register(Order)
# admin.site.register(Service)
admin.site.register(Review)

class MastersCountFilter(admin.SimpleListFilter):
    title = "Количество мастеров"
    parameter_name = "masters_count"

    def lookups(self, request, model_admin):
        return [
            ("0", "Нет мастеров"),
            ("1-3", "От 1 до 3"),
            ("4+", "4 и более"),
        ]

    def queryset(self, request, queryset):
        queryset = queryset.annotate(masters_count=Count("masters"))
        if self.value() == "0":
            return queryset.filter(masters_count=0)
        if self.value() == "1-3":
            return queryset.filter(masters_count__gte=1, masters_count__lte=3)
        if self.value() == "4+":
            return queryset.filter(masters_count__gte=4)
        return queryset

class ServiceAdmin(admin.ModelAdmin):
    

    list_display = ['name','description', 'price', 'duration', 'is_popular', 'masters_count']
    
    search_fields = ['name','description', ]
    list_filter = ['is_popular', 'duration', 'price', MastersCountFilter]
    list_display_links = ['name']
    list_editable = ['is_popular', 'duration', 'price']
    @admin.display(description='Количество мастеров')
    def masters_count(self, obj):
        return obj.masters.count()

    # list_display = ('name', 'price', 'duration', 'is_popular')
    # list_filter = ('is_popular',)
    # search_fields = ('name', 'description')

admin.site.register(Service,ServiceAdmin)

