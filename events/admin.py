from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_datetime", "venue", "is_outreach")
    list_filter = ("is_outreach",)
    search_fields = ("title", "venue")
    prepopulated_fields = {"slug": ("title",)}
