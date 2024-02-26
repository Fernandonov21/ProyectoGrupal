#Establecer ruta de acceso a la vista de la aplicación ejecutar algo cunado una url sea visitada
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
#utilizando esta clase cuando yo lo ejecute me va devolver un formulario 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
# Importar funciones para la autenticación de usuarios en Django, me da un motodo para crear una cookie por nosotros

from django.contrib.auth import login, logout, authenticate
#PARA REGISTRAR USUARIOS IMPORTAMOS EL MODELO DE USUARIO  QUE NO S PERMITE REGISTARAR USUARIOS
from django.contrib.auth.models import User
# Importar excepción para manejar errores de integridad en la base de datos

from django.db import IntegrityError # Maneja la excepción de integridad

from django.utils import timezone
from django.contrib.auth.decorators import login_required #decorador en cada funcion apra proteger

from .models import Queja

from .forms import QuejaForm
# Create your views here.
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm}) 
    else:

        if request.POST["password1"] == request.POST["password2"]: #si las contraseñas coinciden entonces los guardamos

            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user) #user que queremos guardar
                return redirect('quejas')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "El usuario ya existe."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "contraseñas no coinciden."})



@login_required
def quejas(request):
    quejas = Queja.objects.filter(user=request.user, datecompletedqueja__isnull=True) # me devuelve todas las quejas que esten en la base de datos
    return render(request, 'quejas.html', {"quejas": quejas})# pasa el dato al frontend
@login_required
def quejas_completed(request):
    quejas = Queja.objects.filter(user=request.user, datecompletedqueja__isnull=False).order_by('-datecompletedqueja')
    return render(request, 'quejas.html', {"quejas": quejas})




def home(request):
    return render(request, 'home.html')

@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
    if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

    login(request, user)
    return redirect('quejas')

@login_required
def queja_detail(request, queja_id):
    if request.method == 'GET':
        queja = get_object_or_404(Queja, pk=queja_id, user=request.user)
        form = QuejaForm(instance=queja)
        return render(request, 'queja_detail.html', {'queja': queja, 'form': form})
    else:
        try:
            queja = get_object_or_404(Queja, pk=queja_id, user=request.user)
            form = QuejaForm(request.POST, instance=Queja)
            form.save()
            return redirect('quejas')
        except ValueError:
            return render(request, 'queja_detail.html', {'queja': queja, 'form': form, 'error': 'Error updating queja.'})        

# @login_required
@login_required
def complete_queja(request, queja_id):
    queja = get_object_or_404(Queja, pk=queja_id, user=request.user)
    if request.method == 'POST': # si es post lo actualiza
        queja.datecompletedqueja= timezone.now() # si tiene una fecha es que ya se cumplio que la queja esta completa
        queja.save()
        return redirect('quejas')
@login_required
def delete_queja(request, queja_id):
    queja = get_object_or_404(Queja, pk=queja_id, user=request.user)
    if request.method == 'POST':
        queja.delete()
    return redirect('quejas')

# #-------------------
@login_required
def create_queja(request):
        if request.method == "GET":
            return render(request, 'create_queja.html', {"form": QuejaForm})
        else:
            try:
                form = QuejaForm(request.POST)
                new_queja = form.save(commit=False) #que me devuela los datos que estan dentro del formulario
                new_queja.user = request.user
                new_queja.save()
                return redirect('quejas') #redireccionamos
            except ValueError:
                return render(request, 'create_queja.html', {"form": QuejaForm, "error": "Error creating QUEJA."})
