from django.shortcuts import render, redirect
from django.views.generic import View
from todoweb.forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User

# Create your views here.

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        return render(request, "register.html", {"form":form})

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect("register")
        else:
            return render(request, "register.html", {"form":form})

class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        return render(request, "login.html", {"form":form})

