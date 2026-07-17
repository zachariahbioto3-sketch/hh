from django.contrib import admin
from django.utils.html import format_html
from .models import NewsletterSubscriber, Newsletter


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "subscribed", "subscribed_at")
    list_filter = ("subscribed",)
    search_fields = ("email", "name")
    actions = ["subscribe_all", "unsubscribe_all"]

    def subscribe_all(self, request, queryset):
        queryset.update(subscribed=True)
    subscribe_all.short_description = "Subscribe selected subscribers"

    def unsubscribe_all(self, request, queryset):
        queryset.update(subscribed=False)
    unsubscribe_all.short_description = "Unsubscribe selected subscribers"


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("title", "status_display", "recipient_count", "created_at")
    search_fields = ("title", "subject")
    filter_horizontal = ("recipients",)
    actions = ["send_newsletter"]

    def status_display(self, obj):
        if obj.is_sent:
            return format_html(f'<span style="color: green;">✓ Sent {obj.sent_at.strftime("%Y-%m-%d %H:%M")}</span>')
        return format_html('<span style="color: orange;">Draft</span>')
    status_display.short_description = "Status"

    def recipient_count(self, obj):
        return obj.recipients.filter(subscribed=True).count()
    recipient_count.short_description = "Recipients"

    def send_newsletter(self, request, queryset):
        for newsletter in queryset:
            if not newsletter.is_sent:
                newsletter.send()
        self.message_user(request, f"Sent {queryset.count()} newsletter(s)")
    send_newsletter.short_description = "Send selected newsletters"
