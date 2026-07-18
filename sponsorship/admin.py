from django.contrib import admin
from .models import SponsorshipTier, Sponsor, SponsorshipInquiry

admin.site.register(SponsorshipTier)
admin.site.register(Sponsor)

@admin.register(SponsorshipInquiry)
class SponsorshipInquiryAdmin(admin.ModelAdmin):
    list_display  = ('company_name','contact_name','email','responded','submitted_at')
    list_editable = ('responded',)
