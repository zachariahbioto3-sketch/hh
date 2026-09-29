from django.db import models

class ContactMessage(models.Model):
    name         = models.CharField(max_length=100)
    email        = models.EmailField()
    subject      = models.CharField(max_length=200)
    message      = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    read         = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} — {self.subject}"


class Officer(models.Model):
    POSITION_CHOICES = [
        ('chairperson',      'Chairperson'),
        ('vice_chairperson', 'Vice Chairperson'),
        ('secretary',        'Secretary General'),
        ('asst_secretary',   'Assistant Secretary'),
        ('treasurer',        'Treasurer'),
        ('asst_treasurer',   'Assistant Treasurer'),
        ('academic',         'Academic Secretary'),
        ('outreach',         'Outreach Coordinator'),
        ('welfare',          'Welfare Officer'),
        ('prm',              'PRO & Marketing'),
    ]

    name       = models.CharField(max_length=100)
    position   = models.CharField(max_length=30, choices=POSITION_CHOICES)
    order      = models.PositiveIntegerField(default=0, help_text='Display order — lower = first')
    photo      = models.ImageField(upload_to='officers/', blank=True, null=True)
    short_bio  = models.CharField(max_length=160, blank=True, help_text='One line shown on card')
    full_bio   = models.TextField(blank=True, help_text='Full bio shown in modal')
    term       = models.CharField(max_length=50, blank=True, help_text='e.g. 2025/2026')
    quote      = models.CharField(max_length=220, blank=True)
    email      = models.EmailField(blank=True)
    linkedin   = models.URLField(blank=True)
    instagram  = models.URLField(blank=True)
    is_active  = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} — {self.get_position_display()}"
