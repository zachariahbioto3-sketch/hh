from django.urls import path
from . import views

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("<slug:slug>/", views.event_detail, name="event_detail"),
    path("<slug:slug>/rsvp/", views.rsvp_toggle, name="rsvp_toggle"),
    path("<slug:slug>/rsvp/qr/", views.rsvp_qr, name="rsvp_qr"),
    path("<slug:slug>/checkin/", views.checkin_dashboard, name="checkin_dashboard"),
    path("<slug:slug>/checkin/<str:token>/", views.checkin_scan, name="checkin_scan"),
]
