from django import forms
from .models import ContactMessage

INPUT_CLASSES = "font-sans text-[15px] px-3.5 py-3 rounded-xl border border-paperdim bg-white text-ink focus:outline-none focus:border-teal"


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "email": forms.EmailInput(attrs={"class": INPUT_CLASSES}),
            "subject": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "message": forms.Textarea(attrs={"class": INPUT_CLASSES, "rows": 5}),
        }
