from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SponsorshipTier, Sponsor, SponsorshipInquiry

def sponsorship_page(request):
    tiers   = SponsorshipTier.objects.all()
    sponsors = Sponsor.objects.filter(active=True)
    if request.method == 'POST':
        SponsorshipInquiry.objects.create(
            company_name    = request.POST.get('company_name', ''),
            contact_name    = request.POST.get('contact_name', ''),
            email           = request.POST.get('email', ''),
            phone           = request.POST.get('phone', ''),
            message         = request.POST.get('message', ''),
            interested_tier_id = request.POST.get('tier') or None,
        )
        messages.success(request, 'Inquiry received! We will contact you soon.')
        return redirect('sponsorship_page')
    return render(request, 'sponsorship/sponsorship.html', {'tiers': tiers, 'sponsors': sponsors})
