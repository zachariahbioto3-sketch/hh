from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("user", "tier", "status", "has_paid_dues", "date_joined")
    list_filter = ("tier", "status", "has_paid_dues")
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email")
    actions = ["approve_members", "reject_members"]

    def approve_members(self, request, queryset):
        queryset.update(status="approved")
    approve_members.short_description = "Approve selected members"

    def reject_members(self, request, queryset):
        queryset.update(status="rejected")
    reject_members.short_description = "Reject selected members"
