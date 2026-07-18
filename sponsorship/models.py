from django.db import models

class SponsorshipTier(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    benefits    = models.TextField()
    ordering    = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.name


class Sponsor(models.Model):
    name     = models.CharField(max_length=200)
    logo     = models.ImageField(upload_to='sponsors/', blank=True, null=True)
    website  = models.URLField(blank=True)
    tier     = models.ForeignKey(SponsorshipTier, on_delete=models.SET_NULL, null=True, blank=True)
    active   = models.BooleanField(default=True)
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.name


class SponsorshipInquiry(models.Model):
    company_name    = models.CharField(max_length=200)
    contact_name    = models.CharField(max_length=100)
    email           = models.EmailField()
    phone           = models.CharField(max_length=20, blank=True)
    message         = models.TextField()
    interested_tier = models.ForeignKey(SponsorshipTier, on_delete=models.SET_NULL, null=True, blank=True)
    responded       = models.BooleanField(default=False)
    submitted_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.company_name} - {self.contact_name}"
