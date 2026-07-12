from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    TIER_CHOICES = [
        ("student", "Student"),
        ("alumni", "Alumni"),
        ("honorary", "Honorary"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="member_profile")
    year_of_study = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default="student")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="approved")
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="members/", blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    has_paid_dues = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_tier_display()})"

