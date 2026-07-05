from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Member

INPUT_CLASSES = "font-sans text-[15px] px-3.5 py-3 rounded-xl border border-paperdim bg-white text-ink focus:outline-none focus:border-teal w-full"


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": INPUT_CLASSES}))
    year_of_study = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))
    phone_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASSES}))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": INPUT_CLASSES})
        self.fields["password1"].widget.attrs.update({"class": INPUT_CLASSES})
        self.fields["password2"].widget.attrs.update({"class": INPUT_CLASSES})

    def save(self, commit=True):
        user = super().save(commit=commit)
        Member.objects.create(
            user=user,
            year_of_study=self.cleaned_data.get("year_of_study", ""),
            phone_number=self.cleaned_data.get("phone_number", ""),
        )
        return user
