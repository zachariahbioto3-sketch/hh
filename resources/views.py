from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Resource


def _check_access(request):
    member = getattr(request.user, "member_profile", None)
    if member is None or member.status != "approved":
        messages.info(request, "Resources are available to approved KAFUOSA members. Your membership is currently pending review.")
        return False
    return True


@login_required
def resource_list(request):
    if not _check_access(request):
        return redirect("member_profile")

    category = request.GET.get("category")
    resources = Resource.objects.all()
    if category:
        resources = resources.filter(category=category)
    return render(request, "resources/resource_list.html", {
        "resources": resources,
        "categories": Resource.CATEGORY_CHOICES,
        "active_category": category,
    })


@login_required
def resource_detail(request, pk):
    if not _check_access(request):
        return redirect("member_profile")

    resource = get_object_or_404(Resource, pk=pk)
    file_url = resource.file.url
    extension = file_url.rsplit(".", 1)[-1].lower() if "." in file_url else ""
    is_pdf = extension == "pdf"
    is_image = extension in ["jpg", "jpeg", "png", "gif", "webp"]

    return render(request, "resources/resource_detail.html", {
        "resource": resource,
        "is_pdf": is_pdf,
        "is_image": is_image,
    })
