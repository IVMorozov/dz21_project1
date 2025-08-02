from django.shortcuts import render, redirect
from django.contrib.auth import login, logout as auth_logout, authenticate
from django.views.decorators.http import require_POST
from .forms import UserRegisterForm, UserLoginForm
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from .forms import (
    UserRegisterForm,
    UserLoginForm,
    # CustomPasswordChangeForm,
)



class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = "/"

    def form_valid(self, form):
        # Сохраняем пользователя
        user = form.save()
        # Message
        messages.success(
            self.request,
            f"Добро пожаловать, {user.username}! Вы успешно зарегистрировались.",
        )
        # Выполяем авторизацию
        login(self.request, user)
        # Вызываем родительский метод
        return redirect("landing")

    def form_invalid(self, form):
        # Добавляем сообщение об ошибке
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
        return super().form_invalid(form)

class NewLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = UserLoginForm
    redirect_field_name = "landing"

    def form_valid(self, form):
        """Вызывается при успешной аутентификации."""
        # Получаем залогиненного пользователя
        user = form.get_user()
        # Добавляем сообщение об успехе
        messages.success(self.request, f"Добро пожаловать, {user.username}!")
        # Вызываем родительский метод, который выполняет вход и редирект
        
        return super().form_valid(form)
        # return login_required(view_func, redirect_field_name="orders_list")(request, *view_args, **view_kwargs)
    

    def form_invalid(self, form):
        """Вызывается, если форма невалидна (ошибка входа)."""
        # Добавляем сообщение об ошибке
        messages.error(self.request, "Неверное имя пользователя или пароль")
        # Вызываем родительский метод, который снова рендерит страницу с формой
        return super().form_invalid(form)
    


# @require_POST
# def logout_view(request):
#     auth_logout(request)
#     return redirect("landing")


class NewLogoutView(LogoutView):    
    template_name = "users/logout.html"    
    next_page = "logout"
