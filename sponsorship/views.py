from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SponsorshipTier, Sponsor, SponsorshipInquiry
from .forms import SponsorshipInquiryForm


def sponsorship_page(request):
    tiers = SponsorshipTier.objects.all()
    sponsors = Sponsor.objects.filter(active=True)
    form = SponsorshipInquiryForm()

    if request.method == "POST":
        form = SponsorshipInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for your interest! We'll be in touch shortly.")
            return redirect("sponsorship")

    return render(request, "sponsorship/sponsorship.html", {
        "tiers": tiers,
        "sponsors": sponsors,
        "form": form,
    })
