from django.db import models

class NewsletterSubscriber(models.Model):
    email           = models.EmailField(unique=True)
    name            = models.CharField(max_length=100, blank=True)
    subscribed      = models.BooleanField(default=True)
    subscribed_at   = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    title      = models.CharField(max_length=200)
    subject    = models.CharField(max_length=200)
    content    = models.TextField()
    recipients = models.ManyToManyField(NewsletterSubscriber, blank=True)
    sent_at    = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return self.title
