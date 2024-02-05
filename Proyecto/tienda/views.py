from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import LoginForms, UserRegistrationForm
from django.contrib.auth.models import User

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
                    if user.is_superuser:  # Verifica si el usuario es administrador
                        return redirect('admin')
                    else:
                        return redirect('user')  # Redirige a la página de usuario común
                else:
                    return HttpResponse('Usuario no autenticado')
            else:
                return HttpResponse('Credenciales inválidas')
    else:
        form = LoginForms()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def admin(request):
    return render(request, 'tienda/admin.html', {})

@login_required
def user_page(request):
    return render(request, 'tienda/usuario.html', {})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            return render(request, 'tienda/register_done.html',
                          {'new_user':new_user}
            )
        
    
    else:
        user_form = UserRegistrationForm()
    return render(request, 'tienda/register.html', {'user_form': user_form})
