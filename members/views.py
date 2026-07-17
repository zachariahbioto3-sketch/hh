from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm


def signup(request):
    return render(request, "members/signup_closed.html")


def member_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("member_profile")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "members/login.html")


def member_logout(request):
    logout(request)
    return redirect("home")


@login_required
def member_profile(request):
    from .models import Member
    member, created = Member.objects.get_or_create(
        user=request.user,
        defaults={"status": "approved" if request.user.is_superuser else "pending"},
    )
    return render(request, "members/profile.html", {"member": member})
