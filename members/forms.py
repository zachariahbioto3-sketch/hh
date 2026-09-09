from django import forms
from django.contrib.auth.models import User
from .models import Member

class MemberRegistrationForm(forms.Form):
    first_name        = forms.CharField(max_length=50)
    last_name         = forms.CharField(max_length=50)
    email             = forms.EmailField()
    username          = forms.CharField(max_length=150)
    password          = forms.CharField(widget=forms.PasswordInput)
    confirm_password  = forms.CharField(widget=forms.PasswordInput)
    registration_number = forms.CharField(max_length=50)
    phone_number      = forms.CharField(max_length=20, required=False)
    year_of_study     = forms.IntegerField(required=False)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'):
            raise forms.ValidationError('Passwords do not match.')
        if User.objects.filter(username=cleaned.get('username')).exists():
            raise forms.ValidationError('Username already taken.')
        if Member.objects.filter(registration_number=cleaned.get('registration_number')).exists():
            raise forms.ValidationError('Registration number already exists.')
        return cleaned
