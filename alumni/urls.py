from django.urls import path
from . import views
urlpatterns = [
    path('',                             views.alumni_directory,   name='alumni_directory'),
    path('profile/<int:pk>/',            views.alumni_profile,     name='alumni_profile'),
    path('dashboard/',                   views.alumni_dashboard,   name='alumni_dashboard'),
    path('request-mentorship/<int:pk>/', views.request_mentorship, name='request_mentorship'),
]
