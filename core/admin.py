from django.contrib import admin
from django.db.models import Count

# Register your models here.
from .models import Master, Order, Service, Review

# admin.site.register(Master)
# admin.site.register(Order)
# admin.site.register(Service)
# admin.site.register(Review)

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
    actions =['make_popular', 'make_unpopular']
    @admin.display(description='Количество мастеров')
    def masters_count(self, obj):
        return obj.masters.count()

    @admin.action(description='Сделать услуги популярными')
    def make_popular(self, request, queryset):
        queryset.update(is_popular = True)

    @admin.action(description='Сделать услуги непопулярными')
    def make_unpopular(self, request, queryset):
        queryset.update(is_popular = False)

    # list_display = ('name', 'price', 'duration', 'is_popular')
    # list_filter = ('is_popular',)
    # search_fields = ('name', 'description')

admin.site.register(Service,ServiceAdmin)



class OrderAdmin(admin.ModelAdmin):
    list_display = ['client_name','phone', 'comment', 'status', 'master', 'appointment_date'] 
    search_fields = ['client_name','phone', 'appointment_date']
admin.site.register(Order,OrderAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['text','client_name', 'master', 'created', 'rating', 'is_published'] 
    search_fields = ['client_name','master', 'rating']
    list_filter = ['is_published', 'rating', 'master', ]
    list_display_links = ['client_name']
    actions =['make_published', 'make_unpublished']

    @admin.action(description='Снять отзывы с публикации')
    def make_unpublished(self, request, queryset):
        queryset.update(is_published = False)

    @admin.action(description='Опубликовать отзывы')
    def make_published(self, request, queryset):
        queryset.update(is_published = True)

admin.site.register(Review,ReviewAdmin)

class Master_Review_Inline(admin.TabularInline):
    model = Review  
    extra = 1  # Количество пустых форм для отображени

class ServiceCountFilter(admin.SimpleListFilter):
    title = "Количество услуг"
    parameter_name = "service_count"

    def lookups(self, request, model_admin):
        return [
            ("0", "Нет услуг"),
            ("1-3", "От 1 до 3"),
            ("4+", "4 и более"),
        ]

    def queryset(self, request, queryset):
        queryset = queryset.annotate(service_count=Count("services"))
        if self.value() == "0":
            return queryset.filter(service_count=0)
        if self.value() == "1-3":
            return queryset.filter(service_count__gte=1, service_count__lte=3)
        if self.value() == "4+":
            return queryset.filter(service_count__gte=4)
        return queryset



class MasterAdmin(admin.ModelAdmin):
    list_display = ['name','phone', 'address', 'experience', 'is_active', 'service_count'] 
    search_fields = ['name','phone', ]
    inlines = [Master_Review_Inline]
    list_filter = ['name', 'experience', 'is_active', ServiceCountFilter]
    @admin.display(description='Количество услуг')
    def service_count(self, obj):
        return obj.services.count()
admin.site.register(Master,MasterAdmin)