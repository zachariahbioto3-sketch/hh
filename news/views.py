from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Post

def post_list(request):
    category = request.GET.get("category")
    search   = request.GET.get("search", "").strip()
    posts    = Post.objects.all()
    if category:
        posts = posts.filter(category=category)
    if search:
        posts = posts.filter(Q(title__icontains=search) | Q(excerpt__icontains=search) | Q(body__icontains=search))
    return render(request, "news/post_list.html", {"posts": posts, "category": category, "search": search})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "news/post_detail.html", {"post": post})
