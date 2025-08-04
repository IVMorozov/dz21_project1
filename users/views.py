from django.shortcuts import render, redirect
from django.contrib.auth import login, logout as auth_logout, authenticate, get_user_model
from django.views.decorators.http import require_POST
from .forms import UserRegisterForm, UserLoginForm
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView, PasswordChangeDoneView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_not_required, login_required
from django.utils.decorators import method_decorator
from .forms import (
    UserRegisterForm,
    UserLoginForm,
    UserPasswordChangeForm,
    ProfileUserForm
)
from django.contrib.auth.views import (
    LogoutView,
    LoginView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
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
    redirect_authenticated_user = True

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

class UserPasswordChangeView(PasswordChangeView):
    template_name = "users/password_change_form.html"
    form_class = UserPasswordChangeForm
    success_url = "password_changed"
    # next_page = "password_changed"

class CustomPasswordChangeView(PasswordChangeView):
    template_name = "users/password_change_form.html"
    form_class = UserPasswordChangeForm
    success_url = "/"

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.request.user.pk])
    
    def get_object(self, queryset=None):
        return self.request.user
    
class PasswordChangeDoneView(LogoutView):    
    template_name = "users/password_changed.html"    


class PasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    template_name = "users/password_changed.html"
    

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)


class CustomPasswordResetView(PasswordResetView):
    """
    Шаг 2. - Старт процесса сброса пароля - ввод email пользователя
    """

    template_name = "users/password_reset_form.html"
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("password_reset_done")
    email_template_name = "users/password_reset_email.html"

class CustomPasswordResetDoneView(PasswordResetDoneView):
    """
    Шаг 3. - Страничка уведомления об отправке инструкций по сбросу пароля
    """

    template_name = "users/password_reset_done.html"
    # TODO - Есть ли тут success_url?

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Шаг 5. - Ввод нового пароля"""

    template_name = "users/password_reset_confirm.html"
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("password_reset_complete")

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """
    Шаг 6. Сообщение об успешной смене пароля
    """

    template_name = "users/password_reset_complete.html"