from django.urls import path
from . import views
urlpatterns = [
    path('login/',   views.member_login,   name='member_login'),
    path('logout/',  views.member_logout,  name='member_logout'),
    path('profile/', views.member_profile, name='member_profile'),
]
