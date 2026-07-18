from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from events.models import Event
from .forms import ContactForm
from .models import Executive


def home(request):
    upcoming_events = Event.objects.filter(
        start_datetime__gte=timezone.now()
    ).order_by("start_datetime")[:3]

    executives = Executive.objects.filter(is_active=True).order_by("order", "name")

    return render(request, "pages/home.html", {
        "upcoming_events": upcoming_events,
        "executives": executives,
    })


def about(request):
    executives = Executive.objects.filter(is_active=True).order_by("order", "name")
    return render(request, "pages/about.html", {"executives": executives})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            try:
                send_mail(
                    subject=f"KAFUOSA contact form: {form.cleaned_data.get('subject') or 'New message'}",
                    message=form.cleaned_data["message"],
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, "Thanks - your message has been sent.")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})
