import csv
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from members.models import Member
from events.models import Event, RSVP
from pages.models import ContactMessage

@staff_member_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html', {
        'total_members':   Member.objects.count(),
        'approved':        Member.objects.filter(status='approved').count(),
        'pending':         Member.objects.filter(status='pending').count(),
        'total_events':    Event.objects.count(),
        'total_rsvps':     RSVP.objects.count(),
        'unread_messages': ContactMessage.objects.filter(read=False).count(),
    })

@staff_member_required
def export_members(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="members.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name','Email','Reg No','Tier','Status','Joined','Dues Paid'])
    for m in Member.objects.select_related('user').all():
        writer.writerow([m.user.get_full_name(), m.user.email,
                         m.registration_number, m.tier, m.status,
                         m.date_joined, m.has_paid_dues])
    return response

@staff_member_required
def export_rsvps(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rsvps.csv"'
    writer = csv.writer(response)
    writer.writerow(['Event','Member','Checked In','Checked In At'])
    for r in RSVP.objects.select_related('event','member__user').all():
        writer.writerow([r.event.title, str(r.member), r.checked_in, r.checked_in_at])
    return response

@staff_member_required
def export_contacts(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name','Email','Subject','Message','Submitted','Read'])
    for c in ContactMessage.objects.all():
        writer.writerow([c.name, c.email, c.subject, c.message, c.submitted_at, c.read])
    return response
