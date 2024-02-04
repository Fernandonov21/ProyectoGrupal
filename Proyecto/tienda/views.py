from django.shortcuts import render
from .forms import LoginForms
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import *

def user_login(request):
    if request.method == 'POST':
        form = LoginForms(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Usuario autenticado')
                else:
                    return HttpResponse('Usuario no autenticado')
            else:
                return HttpResponse('Credenciales inválidas')
    else:
        form = LoginForms()
    return render(request, 'tienda/login.html', {'form': form})
   