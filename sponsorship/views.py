from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SponsorshipTier, Sponsor, SponsorshipInquiry

def sponsorship_page(request):
    tiers    = SponsorshipTier.objects.all()
    sponsors = Sponsor.objects.filter(active=True)
    if request.method == "POST":
        company_name = request.POST.get("company_name", "").strip()[:200]
        contact_name = request.POST.get("contact_name", "").strip()[:100]
        email        = request.POST.get("email", "").strip()[:254]
        phone        = request.POST.get("phone", "").strip()[:20]
        message      = request.POST.get("message", "").strip()
        tier_id      = request.POST.get("tier") or None
        if not (company_name and contact_name and email and message):
            messages.error(request, "Please fill in all required fields.")
            return render(request, "sponsorship/sponsorship.html", {"tiers": tiers, "sponsors": sponsors})
        SponsorshipInquiry.objects.create(
            company_name       = company_name,
            contact_name       = contact_name,
            email              = email,
            phone              = phone,
            message            = message,
            interested_tier_id = tier_id,
        )
        messages.success(request, "Inquiry received! We will contact you soon.")
        return redirect("sponsorship_page")
    return render(request, "sponsorship/sponsorship.html", {"tiers": tiers, "sponsors": sponsors})
