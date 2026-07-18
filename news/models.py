from django.db import models

class Post(models.Model):
    CATEGORY_CHOICES = [('academic','Academic'),('outreach','Outreach'),('social','Social')]

    title        = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True)
    category     = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='academic')
    excerpt      = models.TextField(max_length=300)
    body         = models.TextField()
    cover_image  = models.ImageField(upload_to='news/', blank=True, null=True)
    published_at = models.DateTimeField()

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
