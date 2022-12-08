from django.shortcuts import render
from django.views.generic import View
from todoweb.forms import UserRegistrationForm

# Create your views here.

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        return render(request, "register.html", {"form":form})

