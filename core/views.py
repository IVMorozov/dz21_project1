from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required


from pickle import FLOAT
from token import NAME, STRING
from django.db.models import Q,  Sum, Count
from .models import Order, Review, Master, Service
from django.db.models import CharField, TextField  
from django.db.models import Transform 

from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import OrderForm, ReviewModelForm
from django.http import JsonResponse
import json
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
import logging
from django.http import Http404

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Собственный класс проверяем юзер из став и юзер из админ
class AdminStaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff and self.request.user.is_active

class LandingView(TemplateView):
    template_name = "landing.html"

class ThanksTemplateView(TemplateView):
    template_name = "thanks.html"

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "make_appointment.html"
    success_url = reverse_lazy("orders_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Создание заявки"
        context["button_text"] = "Сохранить"
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Заявка успешно создана")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Форма заполнена некорректно")
        return super().form_invalid(form)
    
def get_master_services(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            master_id = data.get('master_id')
    
            # master_id = request.GET.get('master_id')
            # try:
            master = Master.objects.get(id=master_id)
            services = master.services.all()
            services_data = [{'id': service.id, 'description': service.description} for service in services]
            return JsonResponse({'services': services_data})
        except Master.DoesNotExist:
            return JsonResponse({'error': 'Master not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    # if request.method == 'POST':
    #     try:
    #         data = json.loads(request.body)
    #         master_id = data.get('master_id')
    #         master = Master.objects.get(id=master_id)
    #         services = master.services.all()
    #         services_data = [{'id': service.id, 'name': service.name} for service in services]
    #         return JsonResponse({'services': services_data})
    #     except Master.DoesNotExist:
    #         return JsonResponse({'error': 'Master not found'}, status=404)
    #     except json.JSONDecodeError:
    #         return JsonResponse({'error': 'Invalid JSON'}, status=400)
    # return JsonResponse({'error': 'Invalid request method'}, status=405)

class AboutTemplateView(TemplateView):
    template_name = "about.html"

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewModelForm
    template_name = "review_form.html"
    success_url = reverse_lazy("thanks")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Оставить отзыв"
        context["button_text"] = "Отправить отзыв"
        return context
    
    def form_valid(self, form):
        # Отправляем сообщение об успешной отправке
        messages.success(self.request, "Отзыв успешно отправлен")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Отправляем сообщение об ошибке
        messages.error(self.request, "Форма заполнена некорректно")
        return super().form_invalid(form)

class MastersListView(ListView):
    model = Master    
    template_name = "masters_list.html"
    context_object_name = "masters"
    ordering = ["-name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Мастера"
        context["masters"] = Master.objects.prefetch_related("services").filter(
            services__isnull=False
        ).distinct()
        return context

    # def get_queryset(self):
    #     # Определим мастеров у которых есть хотя бы одна услуга
    #     masters = Master.objects.prefetch_related("services").filter(
    #         services__isnull=False
    #     ).distinct()
    #     return masters

def services_list(request):  
    query = Service.objects.all()

    context = {
        'services': query,
        'title': 'Барбершоп Дыня'
    }     
    return render(request, 'services.html', context)

class OrderListView(AdminStaffRequiredMixin, ListView):
    model = Order
    template_name = "orders_list.html"    
    context_object_name = "orders"
    ordering = ['-date_created']
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Барбершоп Дыня"        
        return context

    def get_queryset(self):
        
        # Получаем параметры запроса
        q = self.request.GET.get("q")        

        search_by_phone = self.request.GET.get("search_by_phone", "false") == "true"
        search_by_client_name = self.request.GET.get("search_by_client_name", "false") == "true"
        search_by_comment = self.request.GET.get("search_by_comment", "false") == "true"

        # Cоздаем базовый запрос
        query = Order.objects.all()        

        # Создаем базовую Q
        base_q = Q()

        # Серия IF где мы модифицируем базовый запрос в зависимости от чекбоксов и радиокнопок

        if q:
            if search_by_phone:
                base_q |= Q(phone__icontains=q)

            if search_by_client_name:
                base_q |= Q(name__icontains=q)

            if search_by_comment:
                base_q |= Q(comment__icontains=q)
        
        # Объединяем базовый запрос и базовую Q
        query = query.filter(base_q).order_by('-date_created')

        return query

class OrderDetailView(AdminStaffRequiredMixin, DetailView):
    model = Order
    template_name = "order_detail.html"
    context_object_name = 'order'
    pk_url_kwarg = "order_id"    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object  # Получаем текущий объект заказа
        services = order.services.all()
        context['services'] = services  # Получаем все связанные услуги
        context['order_sum'] = sum(service.price for service in services)        
        return context

def reviews(request):  
    # query = Review.objects.all()
    query = Review.objects.filter(is_published=True)


    context = {
        'reviews': query,
        'title': 'Барбершоп Дыня'
	}  
    return render(request, 'reviews.html', context)