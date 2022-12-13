from django.urls import path
from todoweb import views

urlpatterns=[
    path("register", views.RegisterView.as_view(), name="register"),
    path("login", views.LoginView.as_view(), name="signin"),
    path("home", views.IndexView.as_view(), name='home'),
    path("todos/all", views.TodoListView.as_view(), name='todo-list'),
]   