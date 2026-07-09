from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_datetime", "venue", "is_outreach")
    list_filter = ("is_outreach",)
    search_fields = ("title", "venue")
    prepopulated_fields = {"slug": ("title",)}


from .models import RSVP


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ("member", "event", "checked_in", "checked_in_at", "created_at")
    list_filter = ("checked_in", "event")
    search_fields = ("member__user__username", "member__user__first_name", "member__user__last_name")
