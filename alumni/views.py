from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AlumniProfile, MentorshipMatch, JobPosting

def alumni_directory(request):
    profiles = AlumniProfile.objects.filter(member__status="approved")
    return render(request, "alumni/alumni_list.html", {"profiles": profiles})

def alumni_profile(request, pk):
    profile = get_object_or_404(AlumniProfile, pk=pk)
    return render(request, "alumni/profile.html", {"profile": profile})

@login_required
def alumni_dashboard(request):
    member  = getattr(request.user, "member", None)
    profile = getattr(member, "alumni_profile", None) if member else None
    jobs    = JobPosting.objects.filter(active=True)
    return render(request, "alumni/dashboard.html", {"profile": profile, "jobs": jobs})

@login_required
def request_mentorship(request, pk):
    mentor = get_object_or_404(AlumniProfile, pk=pk)
    member = getattr(request.user, "member", None)
    if not member:
        messages.error(request, "You need a member profile to request mentorship.")
        return redirect("alumni_profile", pk=pk)
    if not member.is_approved:
        messages.error(request, "Only approved members can request mentorship.")
        return redirect("alumni_profile", pk=pk)
    _, created = MentorshipMatch.objects.get_or_create(mentor=mentor, mentee=member)
    if created:
        messages.success(request, "Mentorship request sent!")
    else:
        messages.info(request, "You have already requested mentorship from this alumni.")
    return redirect("alumni_profile", pk=pk)
