from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Event


def event_list(request):
    now = timezone.now()
    upcoming = Event.objects.filter(start_datetime__gte=now).order_by("start_datetime")
    past = Event.objects.filter(start_datetime__lt=now).order_by("-start_datetime")
    outreach = Event.objects.filter(is_outreach=True).order_by("-start_datetime")
    return render(request, "events/event_list.html", {
        "upcoming": upcoming,
        "past": past,
        "outreach": outreach,
    })


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, "events/event_detail.html", {"event": event})
