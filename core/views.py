from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from datetime import datetime


# Create your views here.
def landing(request):  
    context = {
        'name': "Дыня"
	}    
    return render(request, 'landing.html', context)


def thanks(request):  
    context = {
        'name': "Дыня"
	}  
    return render(request, 'thanks.html', context)

def orders_list(request):  
    with connection.cursor() as cursor:
        cursor.execute("SELECT client_name, status FROM appointments")
        row = cursor.fetchall()           

    context = {
        'apps': row
	}  
    return render(request, 'orders_list.html', context)


def masters_list(request):  
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM masters")
        row = cursor.fetchall()           

    context = {
        'masters': row
	}  
    return render(request, 'masters_list.html', context)

def order_detail(request, order_id):  
    try:
        with connection.cursor() as cursor:
            querry = f"SELECT * FROM appointments where id = {order_id}"
            cursor.execute(querry)
            row = cursor.fetchall() 
        context = {
            'app': row   
        }  
        
    except IndexError:
        context = {
            'app':HttpResponse("Запись не найдена", status=404)   
        }
        return context
    
    return render(request, 'order_detail.html', context)