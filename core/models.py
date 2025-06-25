from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Service(models.Model):
    name = models.CharField (max_length=200, verbose_name="Название")
    description = models.TextField (blank=True, verbose_name="Описание")
    price = models.DecimalField (max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField (verbose_name="Длительность", help_text="Время выполнения в минутах")
    is_popular = models.BooleanField (default=False, verbose_name="Популярная услуга")
    image = models.ImageField (upload_to="services/", blank=True, verbose_name="Изображение")

    def __str__(self):
        return self
    
class Master(models.Model):
    name = models.CharField (max_length=150, verbose_name="Имя мастера")
    photo = models.ImageField (upload_to="masters/", blank=True, verbose_name="Фотография")
    phone = models.CharField (max_length=20, verbose_name="Телефон мастера")
    address = models.CharField (max_length=255, verbose_name="Адрес")
    experience = models.PositiveIntegerField (verbose_name="Стаж работы", help_text="Опыт работы в годах")
    services = models.ManyToManyField ('Service', related_name="masters", verbose_name="Услуги")
    is_active = models.BooleanField (default=True, verbose_name="Активен")

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"
        ordering = ['name']

class Order(models.Model): 

    STATUS_CHOICES = [
        (1, "новая"),
        (2, "подтвержденная"),
        (3, "отмененная"),
        (4, "выполненная"),
        
    ]
    client_name = models.CharField (max_length=100, verbose_name="Имя клиента")
    phone = models.CharField (max_length=20, verbose_name="Телефон клиента")
    comment = models.TextField (blank=True, verbose_name="Комментарий")
    status = models.CharField (max_length=50, choices=STATUS_CHOICES, default="not_approved", verbose_name="Статус")
    date_created = models.DateTimeField (auto_now_add=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField (auto_now=True, verbose_name="Дата обновления")
    master = models.ForeignKey ('Master', related_name="orders", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Мастер")
    services = models.ManyToManyField ('Service', related_name="orders", verbose_name="Услуги")
    appointment_date = models.DateTimeField (verbose_name="Дата и время записи")

    def __str__(self):
        return f"{self.client_name}, {self.phone}, {self.appointment_date}"
    



    
class Review(models.Model):
    RATING_CHOICES = [
        (1, "Ужасно"),
        (2, "Плохо"),
        (3, "Нормально"),
        (4, "Хорошо"),
        (5, "Отлично"),
    ]
    text = models.TextField (verbose_name="Текст отзыва")
    client_name = models.CharField (max_length=100, blank=True, verbose_name="Имя клиента")
    master = models.ForeignKey (Master, on_delete=models.CASCADE, verbose_name="Мастер")
    photo = models.ImageField (upload_to="reviews/", blank=True, null=True, verbose_name="Фотография")
    created = models.DateTimeField (auto_now_add=True, verbose_name="Дата создания")
    rating = models.PositiveSmallIntegerField (choices=RATING_CHOICES, verbose_name="Оценка") 
    is_published = models.BooleanField (default=True, verbose_name="Опубликован")

    def __str__(self):
        return self