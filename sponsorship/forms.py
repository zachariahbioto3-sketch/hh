from django import forms
from .models import SponsorshipInquiry


class SponsorshipInquiryForm(forms.ModelForm):
    class Meta:
        model = SponsorshipInquiry
        fields = ["company_name", "contact_name", "email", "phone", "interested_tier", "message"]
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "font-sans text-[15px] px-3.5 py-3 rounded-xl border border-paperdim bg-white text-ink focus:outline-none focus:border-teal w-full"}),
            "contact_name": forms.TextInput(attrs={"class": "font-sans text-[15px] px-3.5 py-3 rounded-xl border border-paperdim bg-white text-ink focus:outline-none focus:border-teal w-full"}),
            "email": forms.EmailInput(attrs={"class": "font-sans text-[15px] px-3.5 py-3 rounded-xl border border-paperdim bg-white text-ink focus:outline-none focus:border-teal w-full"}),
            "phone": forms.TextInput(attrs={"class": "font-sans text-[15px] px-3.5 py-3 rounded-xl border border-paperdim bg-white text-ink focus:outline-none focus:border-teal w-full"}),
            "interested_tier": forms.Select(attrs={"class": "font-sans text-[15px] px-3.5 py-3 rounded-xl border border-paperdim bg-white text-ink focus:outline-none focus:border-teal w-full"}),
            "message": forms.Textarea(attrs={"class": "font-sans text-[15px] px-3.5 py-3 rounded-xl border border-paperdim bg-white text-ink focus:outline-none focus:border-teal w-full", "rows": 5}),
        }
