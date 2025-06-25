from django.db import models

# Create your models here.
class Orders(models.Model):
    order_id = models.IntegerField() 
    client_name = models.CharField(max_length=100) 
    client_phone = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=100)                 

    name = models.CharField(max_length=100)  
    def __str__(self):  
        return {self.order_id}, {self.client_name}, {self.client_phone}, {self.date}, {self.status}

class Order_detail(models.Model):  
    title = models.CharField(max_length=200)  
    author = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='books')  
    def __str__(self):  
        return self.title  
    












class Variety(models.Model):
    varietyName = models.CharField(max_length=30)

    def __str__(self):
        return self.varietyName

class Fruits(models.Model):
    name = models.CharField(max_length=255)
    variety = models.ManyToManyField(Variety)

    def __str__(self):
        return self.name
