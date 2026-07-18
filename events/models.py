import hashlib
from django.db import models
from django.utils import timezone
from members.models import Member

class Event(models.Model):
    title           = models.CharField(max_length=200)
    slug            = models.SlugField(unique=True)
    description     = models.TextField()
    venue           = models.CharField(max_length=200)
    start_datetime  = models.DateTimeField()
    end_datetime    = models.DateTimeField()
    cover_image     = models.ImageField(upload_to='events/', blank=True, null=True)
    is_outreach     = models.BooleanField(default=False)
    people_screened = models.PositiveIntegerField(default=0)
    glasses_donated = models.PositiveIntegerField(default=0)
    capacity        = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-start_datetime']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.start_datetime > timezone.now()

    @property
    def spots_left(self):
        if self.capacity is None:
            return None
        return max(0, self.capacity - self.rsvps.count())


class RSVP(models.Model):
    event         = models.ForeignKey(Event,  on_delete=models.CASCADE, related_name='rsvps')
    member        = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='rsvps')
    created_at    = models.DateTimeField(auto_now_add=True)
    checked_in    = models.BooleanField(default=False)
    checked_in_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('event', 'member')

    def __str__(self):
        return f"{self.member} -> {self.event}"

    @property
    def qr_token(self):
        raw = f"{self.event.id}-{self.member.id}-{self.created_at}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]
