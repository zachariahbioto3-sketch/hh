from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Member
from .forms import MemberRegistrationForm, UserForm, ProfileForm, AlumniForm
from alumni.models import AlumniProfile

def member_login(request):
    if request.method == "POST":
        user = authenticate(request,
                            username=request.POST.get("username"),
                            password=request.POST.get("password"))
        if user:
            login(request, user)
            return redirect("members:profile")
        messages.error(request, "Invalid credentials.")
    return render(request, "members/login.html")

def member_logout(request):
    logout(request)
    return redirect("/")

@login_required
def member_profile(request):
    member      = getattr(request.user, "member", None)
    alumni      = getattr(member, "alumni_profile", None) if member else None
    rsvps       = member.rsvps.select_related("event").order_by("-event__start_datetime") if member else []
    mentorships = member.mentorships.select_related("mentor__member__user").filter(active=True) if member else []

    user_form    = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=member)
    alumni_form  = AlumniForm(instance=alumni) if alumni else AlumniForm()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "edit_profile":
            user_form    = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=member)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect("members:profile")
        elif action == "edit_alumni" and alumni:
            alumni_form = AlumniForm(request.POST, instance=alumni)
            if alumni_form.is_valid():
                alumni_form.save()
                messages.success(request, "Alumni info updated.")
                return redirect("members:profile")

    ctx = {
        "member":       member,
        "alumni":       alumni,
        "rsvps":        rsvps,
        "mentorships":  mentorships,
        "user_form":    user_form,
        "profile_form": profile_form,
        "alumni_form":  alumni_form,
    }
    return render(request, "members/profile.html", ctx)

def member_register(request):
    form = MemberRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        d    = form.cleaned_data
        user = User.objects.create_user(
            username   = d["username"],
            email      = d["email"],
            password   = d["password"],
            first_name = d["first_name"],
            last_name  = d["last_name"],
        )
        Member.objects.create(
            user                = user,
            registration_number = d["registration_number"],
            phone_number        = d.get("phone_number", ""),
            year_of_study       = d.get("year_of_study"),
        )
        messages.success(request, "Registration submitted! Await admin approval.")
        return redirect("members:login")
    return render(request, "members/register.html", {"form": form})
