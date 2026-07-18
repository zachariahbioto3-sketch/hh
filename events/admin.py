from django.contrib import admin
from .models import Event, RSVP

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display        = ('title','venue','start_datetime','is_outreach','capacity')
    prepopulated_fields = {'slug':('title',)}

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('event','member','checked_in','checked_in_at')
    list_filter  = ('checked_in','event')
