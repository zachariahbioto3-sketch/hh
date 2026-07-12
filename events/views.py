from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
import qrcode
import io
from .models import Event, RSVP


def _check_access(request):
    member = getattr(request.user, "member_profile", None)
    if member is None or member.status != "approved":
        messages.info(request, "Resources are available to approved KAFUOSA members. Your membership is currently pending review.")
        return False
    return True


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
    user_rsvp = None
    spots_left = None

    if request.user.is_authenticated:
        member = getattr(request.user, "member_profile", None)
        if member:
            user_rsvp = RSVP.objects.filter(event=event, member=member).first()

    if event.capacity:
        taken = event.rsvps.count()
        spots_left = max(event.capacity - taken, 0)

    return render(request, "events/event_detail.html", {
        "event": event,
        "user_rsvp": user_rsvp,
        "spots_left": spots_left,
    })


@login_required
def rsvp_toggle(request, slug):
    event = get_object_or_404(Event, slug=slug)
    member = getattr(request.user, "member_profile", None)

    if member is None or member.status != "approved":
        messages.error(request, "Only approved members can RSVP to events.")
        return redirect("event_detail", slug=slug)

    existing = RSVP.objects.filter(event=event, member=member).first()
    if existing:
        existing.delete()
        messages.success(request, "Your RSVP has been cancelled.")
    else:
        if event.capacity and event.rsvps.count() >= event.capacity:
            messages.error(request, "Sorry, this event is at full capacity.")
        else:
            RSVP.objects.create(event=event, member=member)
            messages.success(request, "You're on the list! Your QR check-in code is on this page.")

    return redirect("event_detail", slug=slug)


@login_required
def rsvp_qr(request, slug):
    event = get_object_or_404(Event, slug=slug)
    member = request.user.member_profile
    rsvp = get_object_or_404(RSVP, event=event, member=member)

    qr_data = f"{request.build_absolute_uri('/')[:-1]}/events/{event.slug}/checkin/{rsvp.qr_token}/"
    img = qrcode.make(qr_data)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")


@login_required
def checkin_scan(request, slug, token):
    if not request.user.is_staff:
        messages.error(request, "Only staff can check in attendees.")
        return redirect("event_detail", slug=slug)

    event = get_object_or_404(Event, slug=slug)
    rsvp = None
    for candidate in event.rsvps.all():
        if candidate.qr_token == token:
            rsvp = candidate
            break

    if rsvp is None:
        messages.error(request, "Invalid or expired QR code.")
    elif rsvp.checked_in:
        messages.info(request, f"{rsvp.member.user.get_full_name() or rsvp.member.user.username} was already checked in at {rsvp.checked_in_at.strftime('%H:%M')}.")
    else:
        rsvp.checked_in = True
        rsvp.checked_in_at = timezone.now()
        rsvp.save()
        messages.success(request, f"Checked in: {rsvp.member.user.get_full_name() or rsvp.member.user.username}")

    return redirect("checkin_dashboard", slug=slug)


@login_required
def checkin_dashboard(request, slug):
    if not request.user.is_staff:
        messages.error(request, "Only staff can access check-in.")
        return redirect("event_detail", slug=slug)

    event = get_object_or_404(Event, slug=slug)
    rsvps = event.rsvps.select_related("member__user").order_by("member__user__first_name")
    return render(request, "events/checkin_dashboard.html", {
        "event": event,
        "rsvps": rsvps,
        "checked_in_count": rsvps.filter(checked_in=True).count(),
    })
