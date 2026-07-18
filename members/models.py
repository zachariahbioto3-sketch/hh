from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    TIER_CHOICES   = [('student','Student'),('alumni','Alumni'),('honorary','Honorary')]
    STATUS_CHOICES = [('pending','Pending'),('approved','Approved'),('rejected','Rejected')]

    user                = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    year_of_study       = models.PositiveIntegerField(null=True, blank=True)
    phone_number        = models.CharField(max_length=20, blank=True)
    registration_number = models.CharField(max_length=50, unique=True)
    tier                = models.CharField(max_length=20, choices=TIER_CHOICES,   default='student')
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    bio                 = models.TextField(blank=True)
    photo               = models.ImageField(upload_to='members/', blank=True, null=True)
    date_joined         = models.DateField(auto_now_add=True)
    has_paid_dues       = models.BooleanField(default=False)

    class Meta:
        ordering = ['user__last_name']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.registration_number})"

    @property
    def is_approved(self):
        return self.status == 'approved'
