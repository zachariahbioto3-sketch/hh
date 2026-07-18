from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, RSVP

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, slug):
    event    = get_object_or_404(Event, slug=slug)
    user_rsvp = None
    if request.user.is_authenticated and hasattr(request.user, 'member'):
        user_rsvp = RSVP.objects.filter(event=event, member=request.user.member).first()
    return render(request, 'events/event_detail.html', {'event': event, 'user_rsvp': user_rsvp})

@login_required
def rsvp_toggle(request, slug):
    event  = get_object_or_404(Event, slug=slug)
    member = getattr(request.user, 'member', None)
    if not member or not member.is_approved:
        messages.error(request, 'Approved members only.')
        return redirect('event_detail', slug=slug)
    rsvp, created = RSVP.objects.get_or_create(event=event, member=member)
    if not created:
        rsvp.delete()
        messages.info(request, 'RSVP cancelled.')
    else:
        messages.success(request, 'RSVP confirmed!')
    return redirect('event_detail', slug=slug)
