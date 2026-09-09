from django.contrib import admin
from .models import AlumniProfile, MentorshipMatch, JobPosting

@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display  = ("member", "graduation_year", "current_employer", "job_title", "available_for_mentoring")
    list_filter   = ("graduation_year", "available_for_mentoring")
    search_fields = ("member__user__first_name", "member__user__last_name", "current_employer")

@admin.register(MentorshipMatch)
class MentorshipMatchAdmin(admin.ModelAdmin):
    list_display = ("mentor", "mentee", "active")
    list_filter  = ("active",)

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display  = ("title", "company", "location", "posted_by", "active")
    list_filter   = ("active",)
    search_fields = ("title", "company")
