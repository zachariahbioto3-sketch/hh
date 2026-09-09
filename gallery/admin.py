from django.contrib import admin
from .models import GalleryAlbum, GalleryPhoto

@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display  = ("title", "created_at")
    search_fields = ("title",)

@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display  = ("album", "caption", "uploaded_at")
    list_filter   = ("album",)
    search_fields = ("caption",)
