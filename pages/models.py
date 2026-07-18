from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.name} - {self.subject or 'No subject'}"


class Executive(models.Model):
    name = models.CharField(max_length=120)
    position = models.CharField(max_length=120)
    photo = models.ImageField(upload_to="executives/", blank=True, null=True)
    bio = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide without deleting.")

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Executive Member"
        verbose_name_plural = "Executive Council"

    def __str__(self):
        return f"{self.name} - {self.position}"
