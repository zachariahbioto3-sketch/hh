from django import forms
from .models import AlumniProfile


class AlumniProfileForm(forms.ModelForm):
    class Meta:
        model = AlumniProfile
        fields = ["graduation_year", "current_employer", "job_title", "bio", "linkedin", "phone", "available_for_mentoring"]
        widgets = {
            "graduation_year": forms.NumberInput(attrs={"class": "font-sans text-[15px] px-3.5 py-3 rounded-xl border border-paperdim bg-white text-ink focus:outline-none focus:border-teal w-full"}),
            "current_employer": forms.TextInput(attrs={"class": "font-sans text-[15px] px-3.5 py-3 rounded-xl border border-paperdim bg-white text-ink focus:outline-none focus:border-teal w-full"}),
            "job_title": forms.TextInput(attrs={"class": "font-sans text-[15px] px-3.5 py-3 rounded-xl border border-paperdim bg-white text-ink focus:outline-none focus:border-teal w-full"}),
            "bio": forms.Textarea(attrs={"class": "font-sans text-[15px] px-3.5 py-3 rounded-xl border border-paperdim bg-white text-ink focus:outline-none focus:border-teal w-full", "rows": 4}),
            "linkedin": forms.URLInput(attrs={"class": "font-sans text-[15px] px-3.5 py-3 rounded-xl border border-paperdim bg-white text-ink focus:outline-none focus:border-teal w-full"}),
            "phone": forms.TextInput(attrs={"class": "font-sans text-[15px] px-3.5 py-3 rounded-xl border border-paperdim bg-white text-ink focus:outline-none focus:border-teal w-full"}),
            "available_for_mentoring": forms.CheckboxInput(attrs={"class": "w-4 h-4"}),
        }
