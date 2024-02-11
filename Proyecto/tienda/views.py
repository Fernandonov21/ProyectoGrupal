from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.models import User
from .models import *
from .utils import get_cart

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
                        return redirect('user_page')  # Redirige a la página de usuario común
                else:
                    return HttpResponse('Usuario no autenticado')
            else:
                return HttpResponse('Credenciales inválidas')
    else:
        form = LoginForms()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def admin(request):
    if request.user.is_authenticated:
        return redirect('users_list')
    else:
        return render(request, 'tienda/admin.html', {})


@login_required
def user_page(request):
    if request.user.is_authenticated:
        # Si el usuario ha iniciado sesión, redirige al menú
        return redirect('menu')
    else:
        return render(request, 'usuario/usuario.html', {})

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
    if request.user.is_superuser:
        template_name = 'tienda/inventario.html'
    else:
        template_name = 'usuario/inventario_user.html'
    context = {
        'categories' : categories,
        'products' : products
    }
    return render(request, template_name, context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product
    }
    return render(request, 'usuario/detail.html', context)


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
    product = get_object_or_404(Product, pk=product_id)
    if request.user.is_superuser:
        template_name = 'tienda/editar_producto.html'
    else:
        template_name = 'usuario/editar_producto_user.html'

    if request.method == 'POST':
        form = ProductEditForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('inventario' if request.user.is_superuser else 'inventario_user')
    else:
        form = ProductEditForm(instance=product)

    return render(request, template_name, {'form': form})     

#Metodos para el usuario

@login_required
def menu(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories' : categories,
        'products' : products
    }
    return render(request, 'usuario/usuario.html', context)



@login_required
def detail_list(request):
    cart = get_cart(request)
    context = {
        'cart': cart
    }

    return render(request, 'cart/detail.html', context)

def cart_detail(request):
    cart = get_cart(request)
    context = {
        'cart': cart
    }
    return render(request, 'cart/detail.html', context)


@login_required
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = get_cart(request)
    quantity = request.POST.get('quantity')
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += int(quantity)
        cart_item.save()
    return redirect('cart-detail')


@login_required
def cart_remove(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return redirect('cart-detail')

@login_required
def cart_update(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    quantity = request.POST.get('quantity')
    cart_item.quantity = quantity
    cart_item.save()
    return redirect('cart-detail')