from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from datetime import datetime


# Create your views here.
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
        cursor.execute("SELECT client_name, status, date  FROM appointments")
        row = cursor.fetchall()           

    context = {
        'apps': row,
        'title': 'Список записей'
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
            querry = f"SELECT * FROM appointments where id = {order_id}"
            cursor.execute(querry)
            row = cursor.fetchall() 
        context = {
            'app': row,
            'title': 'Барбершоп Дыня'   
        }  
        
    except IndexError:
        context = {
            'app':HttpResponse("Запись не найдена", status=404) ,
            'title': 'Барбершоп Дыня'  
        }
        return context
    
    return render(request, 'order_detail.html', context)