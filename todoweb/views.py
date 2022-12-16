from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from todoweb.forms import UserRegistrationForm, UserLoginForm, TodoForm
from django.contrib.auth.models import User
from api.models import Todo
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib import messages

# Create your views here.

def signin_required(fn):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must have login first")
            return redirect('signin')
        else:
            return fn(request, *args, **kwargs)
    return wrapper


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)

            messages.success(request, "Account has been created")
            return redirect("signin")
        else:
            
            messages.error(request, "Sign-up information is not valid")
            return render(request, "register.html", {"form": form})


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        return render(request, "login.html", {"form": form})

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
                
                messages.error(request, "login credentionals are not matching")   
                return redirect('signin')


@method_decorator(signin_required, name="dispatch")
class IndexView(TemplateView):
    # def get(self, request, *args, **kwargs):
    #     return render(request, 'index.html')
    template_name = 'index.html'


@method_decorator(signin_required, name="dispatch")
class TodoListView(View):
    def get(self, request, *args, **kwargs):
        user_todos = Todo.objects.filter(user=request.user)
        return render(request, 'todo-list.html', {"todos": user_todos})


@method_decorator(signin_required, name="dispatch")
class TodoCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TodoForm()
        return render(request, 'todo-create.html', {"form":form})

    def post(self, request, *args, **kwargs):
        form = TodoForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            
            messages.success(request, "Todo created")
            return redirect("todo-list")
        else:
            
            messages.error(request, "Todo is not created")
            return render(request, 'todo-create.html', {'form':form})


@method_decorator(signin_required, name="dispatch")
class TodoDetailsView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        qs = Todo.objects.get(id=id)
        return render(request, 'todo-detail.html', {'todo':qs})


@signin_required
def todo_delete_view(request, *args, **kwargs):
        id = kwargs.get('id')
        Todo.objects.get(id=id).delete()
        
        messages.success(request, "Todo deleted")
        return redirect('todo-list')


@signin_required
def signout_view(request, *args, **kwargs):
    logout(request)
    return redirect("signin")