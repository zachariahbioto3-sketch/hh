from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def member_login(request):
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('member_profile')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'members/login.html')

def member_logout(request):
    logout(request)
    return redirect('/')

@login_required
def member_profile(request):
    member = getattr(request.user, 'member', None)
    return render(request, 'members/profile.html', {'member': member})

from .forms import MemberRegistrationForm

def member_register(request):
    form = MemberRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        d = form.cleaned_data
        user = User.objects.create_user(
            username   = d['username'],
            email      = d['email'],
            password   = d['password'],
            first_name = d['first_name'],
            last_name  = d['last_name'],
        )
        Member.objects.create(
            user                = user,
            registration_number = d['registration_number'],
            phone_number        = d.get('phone_number', ''),
            year_of_study       = d.get('year_of_study'),
        )
        messages.success(request, 'Registration submitted! Await admin approval.')
        return redirect('member_login')
    return render(request, 'members/register.html', {'form': form})
