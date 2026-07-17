from django.db import models


class SponsorshipTier(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    benefits = models.TextField(help_text="List benefits, one per line")
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordering"]

    def __str__(self):
        return f"{self.name} (Ksh {self.price})"

    def get_benefits_list(self):
        return [b.strip() for b in self.benefits.split('\n') if b.strip()]


class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="sponsors/")
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    tier = models.ForeignKey(SponsorshipTier, on_delete=models.SET_NULL, null=True, blank=True)
    joined_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordering", "-joined_date"]

    def __str__(self):
        return self.name


class SponsorshipInquiry(models.Model):
    company_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    interested_tier = models.ForeignKey(SponsorshipTier, on_delete=models.SET_NULL, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.company_name} - {self.contact_name}"
