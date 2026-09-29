from django import forms
from django.contrib.auth.models import User
from .models import Member
from alumni.models import AlumniProfile

class MemberRegistrationForm(forms.Form):
    first_name          = forms.CharField(max_length=50)
    last_name           = forms.CharField(max_length=50)
    email               = forms.EmailField()
    username            = forms.CharField(max_length=150)
    password            = forms.CharField(widget=forms.PasswordInput)
    confirm_password    = forms.CharField(widget=forms.PasswordInput)
    registration_number = forms.CharField(max_length=50)
    phone_number        = forms.CharField(max_length=20, required=False)
    year_of_study       = forms.IntegerField(required=False)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        if User.objects.filter(username=cleaned.get("username")).exists():
            raise forms.ValidationError("Username already taken.")
        if Member.objects.filter(registration_number=cleaned.get("registration_number")).exists():
            raise forms.ValidationError("Registration number already exists.")
        return cleaned

class UserForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "profile-input"}),
            "last_name":  forms.TextInput(attrs={"class": "profile-input"}),
            "email":      forms.EmailInput(attrs={"class": "profile-input"}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model  = Member
        fields = ["bio", "phone_number", "year_of_study", "photo"]
        widgets = {
            "bio":           forms.Textarea(attrs={"class": "profile-input", "rows": 4}),
            "phone_number":  forms.TextInput(attrs={"class": "profile-input"}),
            "year_of_study": forms.NumberInput(attrs={"class": "profile-input"}),
        }

class AlumniForm(forms.ModelForm):
    class Meta:
        model  = AlumniProfile
        fields = ["graduation_year", "current_employer", "job_title", "linkedin", "available_for_mentoring"]
        widgets = {
            "graduation_year":  forms.NumberInput(attrs={"class": "profile-input"}),
            "current_employer": forms.TextInput(attrs={"class": "profile-input"}),
            "job_title":        forms.TextInput(attrs={"class": "profile-input"}),
            "linkedin":         forms.URLInput(attrs={"class": "profile-input"}),
        }
