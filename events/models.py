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
    capacity = models.PositiveIntegerField(blank=True, null=True, help_text="Leave blank for unlimited")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_datetime"]

    def __str__(self):
        return self.title

    @property
    def is_past(self):
        return self.start_datetime < timezone.now()


class RSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="rsvps")
    member = models.ForeignKey("members.Member", on_delete=models.CASCADE, related_name="rsvps")
    checked_in = models.BooleanField(default=False)
    checked_in_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["event", "member"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.member.user.get_full_name() or self.member.user.username} → {self.event.title}"

    @property
    def qr_token(self):
        import hashlib
        raw = f"{self.event.id}-{self.member.id}-{self.created_at}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]
