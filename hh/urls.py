from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/',       admin.site.urls),
    path('',             include('pages.urls')),
    path('members/',     include('members.urls')),
    path('events/',      include('events.urls')),
    path('news/',        include('news.urls')),
    path('resources/',   include('resources.urls')),
    path('gallery/',     include('gallery.urls')),
    path('alumni/',      include('alumni.urls')),
    path('sponsorship/', include('sponsorship.urls')),
    path('newsletter/',  include('newsletter.urls')),
    path('dashboard/',   include('dashboard.urls')),
]
