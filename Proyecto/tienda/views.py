from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.models import User
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


def users_list(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request,'tienda/admin.html', context)


@login_required
def editar_usuario(request, user_id):
    # Obtener el usuario a editar o mostrar un error 404 si no existe
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users_list')
    else:
        form = UserEditForm(instance=user)
    
    return render(request, 'tienda/editar_usuario.html', {'form': form})

@login_required
def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin')
    return render(request, 'tienda/confirm_delete.html', {'user': user})

@login_required
def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories' : categories,
        'products' : products
    }
    return render(request, 'tienda/inventario.html', context)

@login_required
def product_create(request):
    if request.method == ('POST'):
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        category = Category.objects.get(id = category)
        product = Product.objects.create(
            name = name,
            description = description,
            price = price,
            category = category
        )   
        return redirect('inventario')
    context = {
        'categories' : Category.objects.all()
    }
    return render(request, 'tienda/crear_producto.html', context)

@login_required
def editar_producto(request, product_id):
    #obtenemos el usuario y si no existe controlamos con una excepcion 
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductEditForm(request.POST, instance = product)
        if form.is_valid:
            form.save()
            return redirect('inventario')
    else:
        form = ProductEditForm(instance = product) 
    return render(request, 'tienda/editar_producto.html', {'form':form})       


