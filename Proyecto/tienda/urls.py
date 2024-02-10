from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user/', views.user_page, name='user'),
    path('', views.users_list, name='users_list'),  
    path('', views.admin, name='admin'), 
    path('crear_producto/', views.product_create ,name='product_create'),
    path('eliminar-usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('inventario/', views.product_list, name='inventario'),   
    path('editar-usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('editar-producto/<int:product_id>/', views.editar_producto, name='editar_producto'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('register/', views.register, name='register'), 
]
