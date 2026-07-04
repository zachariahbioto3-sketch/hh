from django.db import models


class Resource(models.Model):
    CATEGORY_CHOICES = [
        ("study", "Study Materials"),
        ("past_papers", "Past Papers"),
        ("clinical", "Clinical Guidelines"),
        ("cpd", "CPD Workshop Materials"),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=300, blank=True)
    file = models.FileField(upload_to='resources/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title
