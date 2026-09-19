from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage
from events.models import Event
from news.models import Post
from members.models import Member
from django.utils import timezone


def home(request):
    upcoming_events = Event.objects.filter(
        start_datetime__gte=timezone.now()
    ).order_by('start_datetime')[:3]

    latest_news = Post.objects.order_by('-published_at')[:3]

    stats = {
        'members': Member.objects.filter(status='approved').count(),
        'events': Event.objects.count(),
        'screened': Event.objects.filter(is_outreach=True).aggregate(
            total=__import__('django.db.models', fromlist=['Sum']).Sum('people_screened')
        )['total'] or 0,
        'glasses': Event.objects.filter(is_outreach=True).aggregate(
            total=__import__('django.db.models', fromlist=['Sum']).Sum('glasses_donated')
        )['total'] or 0,
    }

    context = {
        'upcoming_events': upcoming_events,
        'latest_news': latest_news,
        'stats': stats,
    }
    return render(request, 'pages/home.html', context)


def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )
            messages.success(request, 'Your message has been sent. We will get back to you soon.')
            return redirect('pages:contact')
        else:
            messages.error(request, 'Please fill in all fields.')

    return render(request, 'pages/contact.html')