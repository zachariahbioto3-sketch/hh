from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("export/members/", views.export_members, name="export_members"),
    path("export/rsvps/", views.export_rsvps, name="export_rsvps"),
    path("export/contacts/", views.export_contacts, name="export_contacts"),
]
