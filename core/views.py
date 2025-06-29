from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from pickle import FLOAT
from token import NAME, STRING
from django.db.models import Q,  Sum, Count
from .models import Order, Review, Master, Service



# Create your views here.
# def get_main_menu():
#     return[
#         {'name': "Главная", 'url':'landing'},
#         {'name': "О нас", 'url': 'about'},
#         {'name': "Услуги", 'url': 'services_list'},
#         {'name': "Мастера", 'url': 'masters_list'},
#         {'name': "Запись", 'url': 'make_appointment'},
#     ]


def landing(request): 

    context = {
        'name': "Дыня",
        'title': 'Барбершоп Дыня'
	}    
    return render(request, 'landing.html', context)

def thanks(request):  
    context = {
        'name': "Дыня",
        'title': 'Барбершоп Дыня'
	}  
    return render(request, 'thanks.html', context)

def make_appointment(request):  
    context = {
        'name': "Дыня",
        'title': 'Барбершоп Дыня'
	}  
    return render(request, 'make_appointment.html', context)

def about(request):  
    context = {
        'name': "Дыня",
        'title': 'Барбершоп Дыня'
	}  
    return render(request, 'about.html', context)



def masters_list(request):     
    query = Master.objects.all()        

    context = {        
        'masters': query,
        'title': 'Барбершоп Дыня',
	}  
    return render(request, 'masters_list.html', context)

def services_list(request):  
    query = Service.objects.all()

    context = {
        'services': query,
        'title': 'Барбершоп Дыня'
	}     
    return render(request, 'services.html', context)

@login_required(login_url='/')
def orders_list(request): 
    query = Order.objects.all().order_by('-date_created')  

    context = {
        'orders': query,
        'title': 'Барбершоп Дыня'
	}     
    return render(request, 'orders_list.html', context)

@login_required(login_url='/')
def order_detail(request, order_id):  

    query = Order.objects.filter(id = order_id)
    item_list = Service.objects.filter(orders__in=query)
    order_sum = Service.objects.filter(orders__in=query).aggregate(ord_sum=Sum('price'))
    master = Master.objects.filter(orders__in=query)
    master = master[0]
    order_sum = order_sum['ord_sum']
    client = query  

    context = {
        'master': master,
        'client': client,
        'order_sum': order_sum,
        'item_list':item_list,
        'title': 'Барбершоп Дыня'
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
    query = Review.objects.all()

    context = {
        'reviews': query,
        'title': 'Барбершоп Дыня'
	}  
    return render(request, 'reviews.html', context)