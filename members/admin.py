from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display  = ('user','registration_number','tier','status','has_paid_dues')
    list_filter   = ('tier','status','has_paid_dues')
    list_editable = ('status','has_paid_dues')
    search_fields = ('user__first_name','user__last_name','registration_number')
