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
