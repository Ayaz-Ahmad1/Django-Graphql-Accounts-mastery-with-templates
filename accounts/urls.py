from django.urls import path, include
from .views import users_list, me, register, home

urlpatterns = [
    path('users/', users_list, name='users_list'),
    path('me/', me, name='users'),
    path('register/', register, name='register'),
    path('', home, name='home'),

#    path('login/', home, name='register'),
    
]
