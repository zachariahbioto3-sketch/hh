from django.db import models
from members.models import Member


class AlumniProfile(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name="alumni_profile")
    graduation_year = models.IntegerField()
    current_employer = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True, help_text="Professional summary")
    linkedin = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    available_for_mentoring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-graduation_year"]

    def __str__(self):
        return f"{self.member.user.get_full_name()} ({self.graduation_year})"


class MentorshipMatch(models.Model):
    mentor = models.ForeignKey(AlumniProfile, on_delete=models.CASCADE, related_name="mentees")
    mentee = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="mentors")
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ["mentor", "mentee"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.mentor.member.user.get_full_name()} mentoring {self.mentee.user.get_full_name()}"


class JobPosting(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    application_link = models.URLField(blank=True, help_text="Link to apply or company careers page")
    posted_by = models.ForeignKey(AlumniProfile, on_delete=models.CASCADE, related_name="job_postings")
    posted_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-posted_at"]

    def __str__(self):
        return f"{self.title} at {self.company}"
