from django.db import models
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    venue = models.CharField(max_length=200)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='events/', blank=True, null=True)

    is_outreach = models.BooleanField(default=False)
    people_screened = models.PositiveIntegerField(blank=True, null=True)
    glasses_donated = models.PositiveIntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_datetime"]

    def __str__(self):
        return self.title

    @property
    def is_past(self):
        return self.start_datetime < timezone.now()
