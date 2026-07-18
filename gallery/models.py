from django.db import models

class GalleryAlbum(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def cover(self):
        return self.photos.first()


class GalleryPhoto(models.Model):
    album       = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name='photos')
    image       = models.ImageField(upload_to='gallery/')
    caption     = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f"{self.album.title} - {self.caption or self.pk}"
