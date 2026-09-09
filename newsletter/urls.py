from django.urls import path
from . import views
urlpatterns = [
    path("subscribe/",                            views.subscribe,   name="newsletter_subscribe"),
    path("unsubscribe/<str:email>/<str:token>/",  views.unsubscribe, name="newsletter_unsubscribe"),
]
