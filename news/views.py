from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    category = request.GET.get('category')
    posts    = Post.objects.all()
    if category:
        posts = posts.filter(category=category)
    return render(request, 'news/post_list.html', {'posts': posts, 'category': category})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'news/post_detail.html', {'post': post})
