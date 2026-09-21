from django.urls import path
app_name = 'pages'
from . import views



urlpatterns = [
    path('',         views.home,    name='home'),
    path('about/',   views.about,   name='about'),
    path('contact/', views.contact, name='contact'),
]
