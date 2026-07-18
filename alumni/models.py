from django.db import models
from members.models import Member

class AlumniProfile(models.Model):
    member                  = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='alumni_profile')
    graduation_year         = models.PositiveIntegerField()
    current_employer        = models.CharField(max_length=200, blank=True)
    job_title               = models.CharField(max_length=200, blank=True)
    bio                     = models.TextField(blank=True)
    linkedin                = models.URLField(blank=True)
    phone                   = models.CharField(max_length=20, blank=True)
    available_for_mentoring = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member} ({self.graduation_year})"


class MentorshipMatch(models.Model):
    mentor = models.ForeignKey(AlumniProfile, on_delete=models.CASCADE, related_name='mentorships')
    mentee = models.ForeignKey(Member,        on_delete=models.CASCADE, related_name='mentorships')
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('mentor', 'mentee')

    def __str__(self):
        return f"{self.mentor} mentors {self.mentee}"


class JobPosting(models.Model):
    title            = models.CharField(max_length=200)
    company          = models.CharField(max_length=200)
    location         = models.CharField(max_length=200)
    description      = models.TextField()
    application_link = models.URLField()
    posted_by        = models.ForeignKey(AlumniProfile, on_delete=models.CASCADE, related_name='job_postings')
    active           = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.title} at {self.company}"
