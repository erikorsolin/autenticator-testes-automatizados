from django.urls import path
from .views import home, dashboard, user_login, user_register, user_logout, forget_password


urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('forget-password/', forget_password, name='forget_password'),
    path('dashboard/', dashboard, name='dashboard'),
]
