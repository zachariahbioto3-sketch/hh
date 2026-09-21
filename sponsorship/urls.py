from django.urls import path
from . import views

app_name = 'sponsorship'

urlpatterns = [
    path('', views.sponsorship_page, name='list'),
]