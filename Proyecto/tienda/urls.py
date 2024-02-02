from django.urls import path
from .views import *

urlpatterns = [
    path('', user_login, name='login'),  # Usa la función user_login para la ruta de inicio
    path('login/', user_login, name='login')    
]
