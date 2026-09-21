from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('subscribe/',                           views.subscribe,   name='subscribe'),
    path('unsubscribe/<str:email>/<str:token>/', views.unsubscribe, name='unsubscribe'),
]