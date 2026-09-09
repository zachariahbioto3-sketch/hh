from django.contrib import admin
from .models import NewsletterSubscriber, Newsletter

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display  = ("email", "name", "subscribed", "subscribed_at")
    list_filter   = ("subscribed",)
    search_fields = ("email", "name")

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display  = ("title", "subject", "sent_at")
    search_fields = ("title", "subject")
