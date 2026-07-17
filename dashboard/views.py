from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.utils import timezone
from members.models import Member
from events.models import Event, RSVP
from pages.models import ContactMessage
from news.models import Post
import csv


def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)


@login_required
@staff_required
def dashboard(request):
    now = timezone.now()
    
    # Member stats
    total_members = Member.objects.count()
    approved_members = Member.objects.filter(status="approved").count()
    pending_members = Member.objects.filter(status="pending").count()
    
    # Event stats
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(start_datetime__gte=now).count()
    past_events = Event.objects.filter(start_datetime__lt=now).count()
    total_rsvps = RSVP.objects.count()
    checked_in = RSVP.objects.filter(checked_in=True).count()
    
    # Contact submissions
    contact_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.count()  # Track as needed
    
    # Recent activity
    recent_members = Member.objects.order_by("-date_joined")[:5]
    recent_contacts = ContactMessage.objects.order_by("-submitted_at")[:5]
    upcoming = Event.objects.filter(start_datetime__gte=now).order_by("start_datetime")[:5]
    
    context = {
        "total_members": total_members,
        "approved_members": approved_members,
        "pending_members": pending_members,
        "total_events": total_events,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "total_rsvps": total_rsvps,
        "checked_in": checked_in,
        "contact_messages": contact_messages,
        "recent_members": recent_members,
        "recent_contacts": recent_contacts,
        "upcoming": upcoming,
    }
    
    return render(request, "dashboard/dashboard.html", context)


@login_required
@staff_required
def export_members(request):
    members = Member.objects.select_related("user").all()
    
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="members_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(["Name", "Registration Number", "Email", "Tier", "Status", "Date Joined"])
    
    for member in members:
        writer.writerow([
            member.user.get_full_name() or member.user.username,
            member.registration_number,
            member.user.email,
            member.get_tier_display(),
            member.get_status_display(),
            member.date_joined.strftime("%Y-%m-%d"),
        ])
    
    return response


@login_required
@staff_required
def export_rsvps(request):
    rsvps = RSVP.objects.select_related("member__user", "event").all()
    
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="rsvps_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(["Event", "Date", "Member", "Reg No", "RSVP Date", "Checked In", "Checked In At"])
    
    for rsvp in rsvps:
        writer.writerow([
            rsvp.event.title,
            rsvp.event.start_datetime.strftime("%Y-%m-%d %H:%M"),
            rsvp.member.user.get_full_name() or rsvp.member.user.username,
            rsvp.member.registration_number,
            rsvp.created_at.strftime("%Y-%m-%d"),
            "Yes" if rsvp.checked_in else "No",
            rsvp.checked_in_at.strftime("%Y-%m-%d %H:%M") if rsvp.checked_in_at else "",
        ])
    
    return response


@login_required
@staff_required
def export_contacts(request):
    messages = ContactMessage.objects.all()
    
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="contact_messages_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(["Date", "Name", "Email", "Subject", "Message"])
    
    for msg in messages:
        writer.writerow([
            msg.submitted_at.strftime("%Y-%m-%d %H:%M"),
            msg.name,
            msg.email,
            msg.subject,
            msg.message[:100],  # First 100 chars
        ])
    
    return response
