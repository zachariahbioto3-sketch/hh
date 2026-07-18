from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage
from events.models import Event
from news.models import Post
from members.models import Member

def home(request):
    upcoming = Event.objects.order_by('start_datetime')[:3]
    posts    = Post.objects.order_by('-published_at')[:3]
    stats    = {
        'members':         Member.objects.filter(status='approved').count(),
        'events':          Event.objects.count(),
        'people_screened': sum(Event.objects.values_list('people_screened', flat=True)),
        'glasses_donated': sum(Event.objects.values_list('glasses_donated', flat=True)),
    }
    return render(request, 'pages/home.html', {'upcoming': upcoming, 'posts': posts, 'stats': stats})

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name    = request.POST.get('name', ''),
            email   = request.POST.get('email', ''),
            subject = request.POST.get('subject', ''),
            message = request.POST.get('message', ''),
        )
        messages.success(request, 'Message sent! We will get back to you shortly.')
        return redirect('contact')
    return render(request, 'pages/contact.html')
