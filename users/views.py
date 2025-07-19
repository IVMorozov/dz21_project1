from django.shortcuts import render, redirect
from django.contrib.auth import login, logout as auth_logout, authenticate
from django.views.decorators.http import require_POST
from .forms import UserRegisterForm, UserLoginForm
from django.core.exceptions import ValidationError


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("landing")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                user = form.get_user()
            # Аутентификация успешна, выполняем вход
                login(request, user)
                return redirect(request.GET.get("next", "landing")) 
    else:
        form = UserLoginForm()
    return render(request, "users/login.html", {"form": form})
    


@require_POST
def logout_view(request):
    auth_logout(request)
    return redirect("landing")


