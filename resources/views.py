from django.shortcuts import render
from .models import Resource


def resource_list(request):
    category = request.GET.get("category")
    resources = Resource.objects.all()
    if category:
        resources = resources.filter(category=category)
    return render(request, "resources/resource_list.html", {
        "resources": resources,
        "categories": Resource.CATEGORY_CHOICES,
        "active_category": category,
    })
