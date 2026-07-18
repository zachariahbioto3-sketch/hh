from django.shortcuts import render, get_object_or_404
from .models import GalleryAlbum

def gallery_list(request):
    albums = GalleryAlbum.objects.all()
    return render(request, 'gallery/gallery_list.html', {'albums': albums})

def gallery_detail(request, pk):
    album = get_object_or_404(GalleryAlbum, pk=pk)
    return render(request, 'gallery/gallery_detail.html', {'album': album})
