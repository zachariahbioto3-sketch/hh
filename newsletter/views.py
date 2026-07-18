from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from .models import NewsletterSubscriber

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        name  = request.POST.get('name', '').strip()
        if email:
            obj, created = NewsletterSubscriber.objects.get_or_create(email=email)
            obj.name       = name or obj.name
            obj.subscribed = True
            obj.save()
            messages.success(request, 'Subscribed successfully!')
    return redirect(request.META.get('HTTP_REFERER', '/'))

def unsubscribe(request, email):
    try:
        sub = NewsletterSubscriber.objects.get(email=email)
        sub.subscribed      = False
        sub.unsubscribed_at = timezone.now()
        sub.save()
    except NewsletterSubscriber.DoesNotExist:
        pass
    return redirect('/')
