from django.urls import path
from . import views

app_name = 'alumni'

urlpatterns = [
    path('',                             views.alumni_directory,   name='list'),
    path('profile/<int:pk>/',            views.alumni_profile,     name='profile'),
    path('dashboard/',                   views.alumni_dashboard,   name='dashboard'),
    path('request-mentorship/<int:pk>/', views.request_mentorship, name='mentorship'),
]