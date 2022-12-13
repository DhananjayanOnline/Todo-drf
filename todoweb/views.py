from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from todoweb.forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from api.models import Todo
from django.contrib.auth import authenticate, login

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

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            user = authenticate(request, username=uname, password=pwd)
            if user:
                login(request, user)
                return redirect('home')
            else:
                print('invalid user')
                return redirect('signin')

class IndexView(TemplateView):
    # def get(self, request, *args, **kwargs):
    #     return render(request, 'index.html')
    template_name = 'index.html'


class TodoListView(View):
    def get(self, request, *args, **kwargs):
        user_todos = Todo.objects.filter(user=request.user)
        return render(request, 'todo-list.html', {"todos":user_todos})