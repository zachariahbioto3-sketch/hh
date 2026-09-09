from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage
from events.models import Event
from news.models import Post
from members.models import Member

def home(request):
    from django.utils import timezone
    upcoming = Event.objects.filter(start_datetime__gte=timezone.now()).order_by("start_datetime")[:3]
    posts    = Post.objects.order_by("-published_at")[:3]
    stats    = {
        "members":         Member.objects.filter(status="approved").count(),
        "events":          Event.objects.count(),
        "people_screened": sum(Event.objects.values_list("people_screened", flat=True)),
        "glasses_donated": sum(Event.objects.values_list("glasses_donated", flat=True)),
    }
    return render(request, "pages/home.html", {"upcoming": upcoming, "posts": posts, "stats": stats})

def about(request):
    return render(request, "pages/about.html")

def contact(request):
    if request.method == "POST":
        name    = request.POST.get("name", "").strip()[:100]
        email   = request.POST.get("email", "").strip()[:254]
        subject = request.POST.get("subject", "").strip()[:200]
        message = request.POST.get("message", "").strip()
        if not (name and email and subject and message):
            messages.error(request, "All fields are required.")
            return render(request, "pages/contact.html")
        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
        messages.success(request, "Message sent! We will get back to you shortly.")
        return redirect("contact")
    return render(request, "pages/contact.html")
