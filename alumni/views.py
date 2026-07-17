from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AlumniProfile, MentorshipMatch, JobPosting
from .forms import AlumniProfileForm


def alumni_directory(request):
    alumni = AlumniProfile.objects.all()
    mentors = alumni.filter(available_for_mentoring=True)
    jobs = JobPosting.objects.filter(active=True)
    
    return render(request, "alumni/directory.html", {
        "alumni": alumni,
        "mentors": mentors,
        "jobs": jobs,
    })


def alumni_profile(request, pk):
    profile = get_object_or_404(AlumniProfile, pk=pk)
    return render(request, "alumni/profile.html", {"profile": profile})


@login_required
def alumni_dashboard(request):
    member = request.user.member_profile
    alumni_profile = AlumniProfile.objects.filter(member=member).first()
    
    if request.method == "POST":
        form = AlumniProfileForm(request.POST, instance=alumni_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.member = member
            profile.save()
            messages.success(request, "Your alumni profile updated!")
            return redirect("alumni_dashboard")
    else:
        form = AlumniProfileForm(instance=alumni_profile)
    
    mentees = MentorshipMatch.objects.filter(mentor=alumni_profile, active=True) if alumni_profile else []
    mentors = MentorshipMatch.objects.filter(mentee=member, active=True)
    
    return render(request, "alumni/dashboard.html", {
        "form": form,
        "alumni_profile": alumni_profile,
        "mentees": mentees,
        "mentors": mentors,
    })


@login_required
def request_mentorship(request, alumni_id):
    alumni = get_object_or_404(AlumniProfile, pk=alumni_id)
    member = request.user.member_profile
    
    match, created = MentorshipMatch.objects.get_or_create(
        mentor=alumni,
        mentee=member,
        defaults={"active": True}
    )
    
    if created:
        messages.success(request, f"Mentorship request sent to {alumni.member.user.get_full_name()}!")
    else:
        messages.info(request, "You've already requested mentorship from this alumnus.")
    
    return redirect("alumni_profile", pk=alumni_id)
