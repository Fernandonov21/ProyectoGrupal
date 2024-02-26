from django.shortcuts import render, redirect, get_object_or_404
#utilizando esta clase cuando yo lo ejecute me va devolver un formulario 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
# Importar funciones para la autenticación de usuarios en Django, me da un motodo para crear una cookie por nosotros

from django.contrib.auth import login, logout, authenticate
#PARA REGISTRAR USUARIOS IMPORTAMOS EL MODELO DE USUARIO  QUE NO S PERMITE REGISTARAR USUARIOS
from django.contrib.auth.models import User
# Importar excepción para manejar errores de integridad en la base de datos

from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task
from .models import Queja
from .forms import TaskForm
from .forms import QuejaForm
# Create your views here.


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user) #user que queremos guardar
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})

def quejas(request):
    quejas = Queja.objects.filter(user=request.user, datecompletedqueja__isnull=True)
    return render(request, 'quejas.html', {"quejas": quejas})
@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})
def quejas_completed(request):
    quejas = Queja.objects.filter(user=request.user, datecompletedqueja__isnull=False).order_by('-datecompleted')
    return render(request, 'quejas.html', {"quejas": quejas})

@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {"form": TaskForm, "error": "Error creating task."})


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
        return redirect('tasks')

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task.'})
def queja_detail(request, queja_id):
    if request.method == 'GET':
        queja = get_object_or_404(Queja, pk=queja_id, user=request.user)
        form = QuejaForm(instance=queja)
        return render(request, 'queja_detail.html', {'queja': Queja, 'form': form})
    else:
        try:
            queja = get_object_or_404(Queja, pk=queja_id, user=request.user)
            form = QuejaForm(request.POST, instance=queja)
            form.save()
            return redirect('quejas')
        except ValueError:
            return render(request, 'queja_detail.html', {'queja': queja, 'form': form, 'error': 'Error updating queja.'})        

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
def complete_queja(request, queja_id):
    queja = get_object_or_404(Queja, pk=queja_id, user=request.user)
    if request.method == 'POST':
        queja.datecompleted= timezone.now()
        queja.save()
        return redirect('quejas')
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
def delete_queja(request, queja_id):
    queja = get_object_or_404(Queja, pk=queja_id, user=request.user)
    if request.method == 'POST':
        queja.delete()
        return redirect('quejas')
    
#-------------------
@login_required
def create_queja(request):
    if request.method == "GET":
        return render(request, 'create_queja.html', {"form": QuejaForm})
    else:
        try:
            form = QuejaForm(request.POST)
            new_queja = form.save(commit=False)
            new_queja.user = request.user
            new_queja.save()
            return redirect('quejas')
        except ValueError:
            return render(request, 'create_queja.html', {"form": QuejaForm, "error": "Error creating QUEJA."})