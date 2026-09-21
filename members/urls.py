from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('login/',    views.member_login,    name='login'),
    path('logout/',   views.member_logout,   name='logout'),
    path('profile/',  views.member_profile,  name='profile'),
    path('register/', views.member_register, name='register'),
]