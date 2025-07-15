from django import forms
from .models import Order, Service, Review, Master
from django.core.exceptions import ValidationError
import re
from datetime import date
from django.forms.widgets import DateInput, TimeInput, DateTimeInput


class ReviewModelForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["client_name", "text", "master", "photo", "rating"]
        widgets = {
            "client_name": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control"}),
            "master": forms.Select(attrs={"class": "form-control"}),
            "rating": forms.Select(attrs={"class": "form-control"}),
        }


class OrderForm(forms.ModelForm):    
    appointment_date = forms.SplitDateTimeField(label="Дата и время записи", widget=forms.SplitDateTimeWidget(attrs={"class": "form-control"}, date_attrs={'class':'datepicker', 'type':'date'}, time_attrs={'class':'timepicker', 'type':'time'},))

    class Meta:
        model = Order

        fields = ["client_name", "phone", "comment", "master", "services", "appointment_date"]
        # fields = '__all__'
        widgets = {
            "client_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control"}),
            "master": forms.Select(attrs={"class": "form-control"}),
            "services": forms.SelectMultiple(attrs={"class": "form-control"}), 
            # "appointment_date":'appointment_date',
            # "appointment_date": forms.SplitDateTimeWidget(attrs={"class": "form-control"}, date_attrs={'class':'datepicker', 'type':'date'}, time_attrs={'class':'timepicker', 'type':'time'},)
        }

    def clean_services(self):
        master = self.cleaned_data.get('master')
        services = self.cleaned_data.get('services')

        if master and services:
            master_services = master.services.all()
            for service in services:
                if service not in master_services:
                    raise ValidationError(f'Мастер {master} не предоставляет услугу "{service}".')
        return services

