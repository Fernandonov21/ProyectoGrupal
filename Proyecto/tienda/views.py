from django.shortcuts import render
from forms import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

# Create your views here.

def user_login(request):
    if request.method == 'POST': #aqui validamos que el request sea un post para guardar información
        form = LoginForms(request.POST)
        if form.is_valid():
            cd = form.changed_data
            user = authenticate(request,
                                username = cd['username'],
                                password = cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('usuario autenticado')
                else:
                    return HttpResponse('usuario no autenticado')
            else:
                 return HttpResponse('usuario no existe')
    else:
        form = LoginForms()
        return render(request, 'account/login.html', {'form':form})        