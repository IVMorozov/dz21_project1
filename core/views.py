from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from datetime import datetime
from django.urls import reverse


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
        "user": {
            "name": "Илья",
            "is_stuff": True
        },
        
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

def orders_list(request):  
    with connection.cursor() as cursor:
        
        querry = f"SELECT a.id, client_name,  client_phone, date, status, count(s.title)  FROM appointments a  JOIN appointments_services a_s on a.id = a_s.appointment_id JOIN services s on a_s.service_id = s.id GROUP BY a.id, a.client_name, a.client_phone, a.date, a.status"
        
        cursor.execute(querry)
        row = cursor.fetchall() 
            
        querry2 = f"SELECT a_s.appointment_id, title, description, price FROM services s JOIN appointments_services a_s on s.id = a_s.service_id"

        cursor.execute(querry2)
        row2 = cursor.fetchall() 

        # querry3 = f"SELECT a_s.appointment_id,  sum(price) FROM services s JOIN appointments_services a_s on s.id = a_s.service_id where a_s.appointment_id = {a.id}"

        # cursor.execute(querry3)
        # row3 = cursor.fetchone() 
        

    context = {
        'apps': row,
        'order_details': row2,
        # 'order_sum': row3, 
        'title': 'Барбершоп Дыня'
	}  
    return render(request, 'orders_list.html', context)

def masters_list(request):  
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM masters")
        row = cursor.fetchall()           

    context = {
        
        'masters': row,
        'title': 'Барбершоп Дыня'
	}  
    return render(request, 'masters_list.html', context)

def services_list(request):  
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM services")
        row = cursor.fetchall()           

    context = {
        'services': row,
        'title': 'Барбершоп Дыня'
	}  
    return render(request, 'services.html', context)

def order_detail(request, order_id):  
    try:
        with connection.cursor() as cursor:            
            querry = f"SELECT a_s.appointment_id, title, description, price FROM services s JOIN appointments_services a_s on s.id = a_s.service_id where a_s.appointment_id = {order_id}"

            cursor.execute(querry)
            row = cursor.fetchall() 

            querry1 = f"SELECT a_s.appointment_id,  sum(price) FROM services s JOIN appointments_services a_s on s.id = a_s.service_id where a_s.appointment_id = {order_id}"

            cursor.execute(querry1)
            row1 = cursor.fetchone() 

        context = {
            'order_details': row,
            'order_sum': row1,            
            'title': 'Барбершоп Дыня'   
        }  
        
    except IndexError:
        context = {
            'app':HttpResponse("Запись не найдена", status=404) ,
            'title': 'Барбершоп Дыня'  
        }
        return context
    
    return render(request, 'order_detail.html', context)

