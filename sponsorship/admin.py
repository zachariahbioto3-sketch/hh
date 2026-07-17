from django.contrib import admin
from .models import SponsorshipTier, Sponsor, SponsorshipInquiry


@admin.register(SponsorshipTier)
class SponsorshipTierAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "ordering")
    list_editable = ("ordering",)


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ("name", "tier", "active", "joined_date", "ordering")
    list_filter = ("active", "tier")
    list_editable = ("ordering",)
    search_fields = ("name",)


@admin.register(SponsorshipInquiry)
class SponsorshipInquiryAdmin(admin.ModelAdmin):
    list_display = ("company_name", "contact_name", "email", "interested_tier", "responded", "submitted_at")
    list_filter = ("responded", "interested_tier")
    search_fields = ("company_name", "contact_name", "email")
    actions = ["mark_responded"]

    def mark_responded(self, request, queryset):
        queryset.update(responded=True)
    mark_responded.short_description = "Mark as responded"
