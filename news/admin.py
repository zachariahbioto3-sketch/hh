from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_at")
    list_filter = ("category",)
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
