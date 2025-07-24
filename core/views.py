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

# Собственный класс проверяем юзер из став и юзер из админ

class AdminStaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff and self.request.user.is_active

class LandingView(TemplateView):
    template_name = "landing.html"

class ThanksTemplateView(TemplateView):
    template_name = "thanks.html"

def make_appointment(request): 
    form = OrderForm(request.POST)
    if not form.is_valid():
            context = {
                "title": "Запись на услуги",
                "button_text": "Записаться",
                "form": form,
            }
            messages.error(request, "Форма заполнена некорректно")
            return render(request, "make_appointment.html", context)

    form.save()
    messages.success(request, "Заявка успешно создана")
    return redirect("thanks")

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

def review_create(request):
    if request.method == "GET":
        form = ReviewModelForm()
        context = {
            "title": "Оставить отзыв",
            "button_text": "Отправить отзыв",
            "form": form,
        }
        
        return render(request, "review_form.html", context)

    elif request.method == "POST":
        form = ReviewModelForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "title": "Оставить отзыв",
                "button_text": "Отправить отзыв",
                "form": form,
            }
            messages.error(request, "Форма заполнена некорректно")
            return render(request, "review_form.html", context)

        form.save()
        messages.success(request, "Отзыв успешно отправлен")
        return redirect("thanks")

class MastersListView(ListView):
    model = Master    
    template_name = "masters_list.html"
    context_object_name = "masters"
    ordering = ["-name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Мастера"
        return context

    def get_queryset(self):
        # Определим мастеров у которых есть хотя бы одна услуга
        masters = Master.objects.prefetch_related("services").filter(
            services__isnull=False
        ).distinct()
        return masters

def services_list(request):  
    query = Service.objects.all()

    context = {
        'services': query,
        'title': 'Барбершоп Дыня'
    }     
    return render(request, 'services.html', context)

# @user_passes_test(lambda u: u.is_staff)
class OrderListView(AdminStaffRequiredMixin, ListView):
    model = Order
    template_name = "orders_list.html"    
    context_object_name = "orders"
    
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

        # Радиокнопки направления сорртировки по дате
        
        order_by_date = self.request.GET.get("order_by_date_created", "desc")

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
        query = query.filter(base_q)

        return query


@login_required(login_url='/')
def order_detail(request, order_id):  
    

    query = Order.objects.filter(id = order_id)
    item_list = Service.objects.filter(orders__in=query)
    order_sum = Service.objects.filter(orders__in=query).aggregate(ord_sum=Sum('price'))
    master = Master.objects.filter(orders__in=query)
    # master_id = request.GET.get('master_id')

    master = master[0]
    order_sum = order_sum['ord_sum']
    client = query  

    context = {
        'master': master,
        'client': client,
        'order_sum': order_sum,
        'item_list':item_list,
        'title': 'Барбершоп Дыня',
        # 'mm': master_id
    } 

    # try:
    #     with connection.cursor() as cursor:            
    #         querry = f"SELECT a_s.appointment_id, title, description, price FROM services s JOIN appointments_services a_s on s.id = a_s.service_id where a_s.appointment_id = {order_id}"

    #         cursor.execute(querry)
    #         row = cursor.fetchall() 

    #         querry1 = f"SELECT a_s.appointment_id,  sum(price) FROM services s JOIN appointments_services a_s on s.id = a_s.service_id where a_s.appointment_id = {order_id}"

    #         cursor.execute(querry1)
    #         row1 = cursor.fetchone() 

    #     context = {
    #         'order_details': row,
    #         'order_sum': row1,            
    #         'title': 'Барбершоп Дыня'   
    #     }  
        
    # except IndexError:
    #     context = {
    #         'app':HttpResponse("Запись не найдена", status=404) ,
    #         'title': 'Барбершоп Дыня'  
    #     }
    #     return context
    
    return render(request, 'order_detail.html', context)

def reviews(request):  
    # query = Review.objects.all()
    query = Review.objects.filter(is_published=True)


    context = {
        'reviews': query,
        'title': 'Барбершоп Дыня'
	}  
    return render(request, 'reviews.html', context)