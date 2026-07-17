from django.db import models
from django.utils import timezone


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    subscribed = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200, help_text="Email subject line")
    content = models.TextField(help_text="HTML or plain text email content")
    recipients = models.ManyToManyField(NewsletterSubscriber, blank=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_sent(self):
        return self.sent_at is not None

    def send(self):
        from django.core.mail import send_mass_mail
        messages = []
        for subscriber in self.recipients.filter(subscribed=True):
            messages.append(
                (self.subject, self.content, 'noreply@kafuosa.org', [subscriber.email])
            )
        if messages:
            send_mass_mail(messages, fail_silently=False)
        self.sent_at = timezone.now()
        self.save()
