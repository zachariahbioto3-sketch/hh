from django.contrib import admin
from .models import AlumniProfile, MentorshipMatch, JobPosting


@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = ("member", "graduation_year", "current_employer", "available_for_mentoring")
    list_filter = ("graduation_year", "available_for_mentoring")
    search_fields = ("member__user__first_name", "member__user__last_name", "current_employer")


@admin.register(MentorshipMatch)
class MentorshipMatchAdmin(admin.ModelAdmin):
    list_display = ("mentor", "mentee", "active", "created_at")
    list_filter = ("active",)
    search_fields = ("mentor__member__user__first_name", "mentee__user__first_name")


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "posted_by", "active", "posted_at")
    list_filter = ("active", "posted_at")
    search_fields = ("title", "company", "location")
