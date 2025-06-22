from django.shortcuts import render, get_object_or_404 
from django.http import HttpResponse
# from .models import Post
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

def order_detail(request, order_id):  
    # app_id = request.GET.get(order_id)
    with connection.cursor() as cursor:
        quer = f"SELECT * FROM appointments where id = {order_id}"
        cursor.execute(quer)
        row = cursor.fetchall()   
    context = {
        'app': row   
	    }

    return render(request, 'order_detail.html', context)
# 