from django.shortcuts import render, get_object_or_404
from .models import GalleryAlbum

def gallery_list(request):
    albums = GalleryAlbum.objects.prefetch_related('photos').all()
    total_photos = sum(a.photos.count() for a in albums)
    return render(request, 'gallery/gallery_list.html', {
        'albums': albums,
        'total_photos': total_photos,
    })

def album_detail(request, pk):
    album = get_object_or_404(GalleryAlbum, pk=pk)
    return render(request, 'gallery/album_detail.html', {'album': album})
