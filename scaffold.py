import os, pathlib

BASE = pathlib.Path('.')

def w(path, text):
    p = BASE / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.lstrip('\n'), encoding='utf-8')
    print(f'  OK  {path}')

w('hh/settings.py', """
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY    = config('SECRET_KEY')
DEBUG         = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'pages',
    'members',
    'events',
    'news',
    'resources',
    'gallery',
    'alumni',
    'sponsorship',
    'newsletter',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hh.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]

WSGI_APPLICATION = 'hh.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Africa/Nairobi'
USE_I18N      = True
USE_TZ        = True

STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'default':    {'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage'},
    'staticfiles':{'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default=''),
    'API_KEY':    config('CLOUDINARY_API_KEY',    default=''),
    'API_SECRET': config('CLOUDINARY_API_SECRET', default=''),
}

MEDIA_URL = '/media/'

LOGIN_URL             = 'member_login'
LOGIN_REDIRECT_URL    = 'member_profile'
LOGOUT_REDIRECT_URL   = '/'

EMAIL_BACKEND       = config('EMAIL_BACKEND',       default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST          = config('EMAIL_HOST',           default='')
EMAIL_PORT          = config('EMAIL_PORT',           default=587, cast=int)
EMAIL_USE_TLS       = config('EMAIL_USE_TLS',        default=True, cast=bool)
EMAIL_HOST_USER     = config('EMAIL_HOST_USER',      default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD',  default='')
DEFAULT_FROM_EMAIL  = config('DEFAULT_FROM_EMAIL',   default='noreply@kafuosa.org')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
""")

w('hh/urls.py', """
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/',       admin.site.urls),
    path('',             include('pages.urls')),
    path('members/',     include('members.urls')),
    path('events/',      include('events.urls')),
    path('news/',        include('news.urls')),
    path('resources/',   include('resources.urls')),
    path('gallery/',     include('gallery.urls')),
    path('alumni/',      include('alumni.urls')),
    path('sponsorship/', include('sponsorship.urls')),
    path('newsletter/',  include('newsletter.urls')),
    path('dashboard/',   include('dashboard.urls')),
]
""")

w('pages/models.py', """
from django.db import models

class ContactMessage(models.Model):
    name         = models.CharField(max_length=100)
    email        = models.EmailField()
    subject      = models.CharField(max_length=200)
    message      = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    read         = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} — {self.subject}"
""")

w('members/models.py', """
from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    TIER_CHOICES   = [('student','Student'),('alumni','Alumni'),('honorary','Honorary')]
    STATUS_CHOICES = [('pending','Pending'),('approved','Approved'),('rejected','Rejected')]

    user                = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    year_of_study       = models.PositiveIntegerField(null=True, blank=True)
    phone_number        = models.CharField(max_length=20, blank=True)
    registration_number = models.CharField(max_length=50, unique=True)
    tier                = models.CharField(max_length=20, choices=TIER_CHOICES,   default='student')
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    bio                 = models.TextField(blank=True)
    photo               = models.ImageField(upload_to='members/', blank=True, null=True)
    date_joined         = models.DateField(auto_now_add=True)
    has_paid_dues       = models.BooleanField(default=False)

    class Meta:
        ordering = ['user__last_name']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.registration_number})"

    @property
    def is_approved(self):
        return self.status == 'approved'
""")

w('events/models.py', """
import hashlib
from django.db import models
from django.utils import timezone
from members.models import Member

class Event(models.Model):
    title           = models.CharField(max_length=200)
    slug            = models.SlugField(unique=True)
    description     = models.TextField()
    venue           = models.CharField(max_length=200)
    start_datetime  = models.DateTimeField()
    end_datetime    = models.DateTimeField()
    cover_image     = models.ImageField(upload_to='events/', blank=True, null=True)
    is_outreach     = models.BooleanField(default=False)
    people_screened = models.PositiveIntegerField(default=0)
    glasses_donated = models.PositiveIntegerField(default=0)
    capacity        = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-start_datetime']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.start_datetime > timezone.now()

    @property
    def spots_left(self):
        if self.capacity is None:
            return None
        return max(0, self.capacity - self.rsvps.count())


class RSVP(models.Model):
    event         = models.ForeignKey(Event,  on_delete=models.CASCADE, related_name='rsvps')
    member        = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='rsvps')
    created_at    = models.DateTimeField(auto_now_add=True)
    checked_in    = models.BooleanField(default=False)
    checked_in_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('event', 'member')

    def __str__(self):
        return f"{self.member} -> {self.event}"

    @property
    def qr_token(self):
        raw = f"{self.event.id}-{self.member.id}-{self.created_at}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]
""")

w('news/models.py', """
from django.db import models

class Post(models.Model):
    CATEGORY_CHOICES = [('academic','Academic'),('outreach','Outreach'),('social','Social')]

    title        = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True)
    category     = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='academic')
    excerpt      = models.TextField(max_length=300)
    body         = models.TextField()
    cover_image  = models.ImageField(upload_to='news/', blank=True, null=True)
    published_at = models.DateTimeField()

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
""")

w('resources/models.py', """
from django.db import models

class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('study','Study Material'),('past_papers','Past Papers'),
        ('clinical','Clinical'),('cpd','CPD'),
    ]
    title       = models.CharField(max_length=200)
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='study')
    description = models.TextField(blank=True)
    file        = models.FileField(upload_to='resources/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title
""")

w('gallery/models.py', """
from django.db import models

class GalleryAlbum(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def cover(self):
        return self.photos.first()


class GalleryPhoto(models.Model):
    album       = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name='photos')
    image       = models.ImageField(upload_to='gallery/')
    caption     = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f"{self.album.title} - {self.caption or self.pk}"
""")

w('alumni/models.py', """
from django.db import models
from members.models import Member

class AlumniProfile(models.Model):
    member                  = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='alumni_profile')
    graduation_year         = models.PositiveIntegerField()
    current_employer        = models.CharField(max_length=200, blank=True)
    job_title               = models.CharField(max_length=200, blank=True)
    bio                     = models.TextField(blank=True)
    linkedin                = models.URLField(blank=True)
    phone                   = models.CharField(max_length=20, blank=True)
    available_for_mentoring = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member} ({self.graduation_year})"


class MentorshipMatch(models.Model):
    mentor = models.ForeignKey(AlumniProfile, on_delete=models.CASCADE, related_name='mentorships')
    mentee = models.ForeignKey(Member,        on_delete=models.CASCADE, related_name='mentorships')
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('mentor', 'mentee')

    def __str__(self):
        return f"{self.mentor} mentors {self.mentee}"


class JobPosting(models.Model):
    title            = models.CharField(max_length=200)
    company          = models.CharField(max_length=200)
    location         = models.CharField(max_length=200)
    description      = models.TextField()
    application_link = models.URLField()
    posted_by        = models.ForeignKey(AlumniProfile, on_delete=models.CASCADE, related_name='job_postings')
    active           = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.title} at {self.company}"
""")

w('sponsorship/models.py', """
from django.db import models

class SponsorshipTier(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    benefits    = models.TextField()
    ordering    = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.name


class Sponsor(models.Model):
    name     = models.CharField(max_length=200)
    logo     = models.ImageField(upload_to='sponsors/', blank=True, null=True)
    website  = models.URLField(blank=True)
    tier     = models.ForeignKey(SponsorshipTier, on_delete=models.SET_NULL, null=True, blank=True)
    active   = models.BooleanField(default=True)
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.name


class SponsorshipInquiry(models.Model):
    company_name    = models.CharField(max_length=200)
    contact_name    = models.CharField(max_length=100)
    email           = models.EmailField()
    phone           = models.CharField(max_length=20, blank=True)
    message         = models.TextField()
    interested_tier = models.ForeignKey(SponsorshipTier, on_delete=models.SET_NULL, null=True, blank=True)
    responded       = models.BooleanField(default=False)
    submitted_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.company_name} - {self.contact_name}"
""")

w('newsletter/models.py', """
from django.db import models

class NewsletterSubscriber(models.Model):
    email           = models.EmailField(unique=True)
    name            = models.CharField(max_length=100, blank=True)
    subscribed      = models.BooleanField(default=True)
    subscribed_at   = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    title      = models.CharField(max_length=200)
    subject    = models.CharField(max_length=200)
    content    = models.TextField()
    recipients = models.ManyToManyField(NewsletterSubscriber, blank=True)
    sent_at    = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return self.title
""")

w('dashboard/models.py', "# No models — staff-only views aggregating stats from all other apps.\n")

w('pages/views.py', """
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage
from events.models import Event
from news.models import Post
from members.models import Member

def home(request):
    upcoming = Event.objects.order_by('start_datetime')[:3]
    posts    = Post.objects.order_by('-published_at')[:3]
    stats    = {
        'members':         Member.objects.filter(status='approved').count(),
        'events':          Event.objects.count(),
        'people_screened': sum(Event.objects.values_list('people_screened', flat=True)),
        'glasses_donated': sum(Event.objects.values_list('glasses_donated', flat=True)),
    }
    return render(request, 'pages/home.html', {'upcoming': upcoming, 'posts': posts, 'stats': stats})

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name    = request.POST.get('name', ''),
            email   = request.POST.get('email', ''),
            subject = request.POST.get('subject', ''),
            message = request.POST.get('message', ''),
        )
        messages.success(request, 'Message sent! We will get back to you shortly.')
        return redirect('contact')
    return render(request, 'pages/contact.html')
""")

w('members/views.py', """
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def member_login(request):
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('member_profile')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'members/login.html')

def member_logout(request):
    logout(request)
    return redirect('/')

@login_required
def member_profile(request):
    member = getattr(request.user, 'member', None)
    return render(request, 'members/profile.html', {'member': member})
""")

w('events/views.py', """
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, RSVP

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, slug):
    event    = get_object_or_404(Event, slug=slug)
    user_rsvp = None
    if request.user.is_authenticated and hasattr(request.user, 'member'):
        user_rsvp = RSVP.objects.filter(event=event, member=request.user.member).first()
    return render(request, 'events/event_detail.html', {'event': event, 'user_rsvp': user_rsvp})

@login_required
def rsvp_toggle(request, slug):
    event  = get_object_or_404(Event, slug=slug)
    member = getattr(request.user, 'member', None)
    if not member or not member.is_approved:
        messages.error(request, 'Approved members only.')
        return redirect('event_detail', slug=slug)
    rsvp, created = RSVP.objects.get_or_create(event=event, member=member)
    if not created:
        rsvp.delete()
        messages.info(request, 'RSVP cancelled.')
    else:
        messages.success(request, 'RSVP confirmed!')
    return redirect('event_detail', slug=slug)
""")

w('news/views.py', """
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    category = request.GET.get('category')
    posts    = Post.objects.all()
    if category:
        posts = posts.filter(category=category)
    return render(request, 'news/post_list.html', {'posts': posts, 'category': category})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'news/post_detail.html', {'post': post})
""")

w('resources/views.py', """
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Resource

def _approved(request):
    member = getattr(request.user, 'member', None)
    return member and member.is_approved

@login_required
def resource_list(request):
    if not _approved(request):
        return HttpResponseForbidden('Approved members only.')
    resources = Resource.objects.all()
    return render(request, 'resources/resource_list.html', {'resources': resources})

@login_required
def resource_detail(request, pk):
    if not _approved(request):
        return HttpResponseForbidden('Approved members only.')
    resource = get_object_or_404(Resource, pk=pk)
    return render(request, 'resources/resource_detail.html', {'resource': resource})
""")

w('gallery/views.py', """
from django.shortcuts import render, get_object_or_404
from .models import GalleryAlbum

def gallery_list(request):
    albums = GalleryAlbum.objects.all()
    return render(request, 'gallery/gallery_list.html', {'albums': albums})

def gallery_detail(request, pk):
    album = get_object_or_404(GalleryAlbum, pk=pk)
    return render(request, 'gallery/gallery_detail.html', {'album': album})
""")

w('alumni/views.py', """
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AlumniProfile, MentorshipMatch, JobPosting

def alumni_directory(request):
    profiles = AlumniProfile.objects.filter(member__status='approved')
    return render(request, 'alumni/directory.html', {'profiles': profiles})

def alumni_profile(request, pk):
    profile = get_object_or_404(AlumniProfile, pk=pk)
    return render(request, 'alumni/profile.html', {'profile': profile})

@login_required
def alumni_dashboard(request):
    member  = getattr(request.user, 'member', None)
    profile = getattr(member, 'alumni_profile', None) if member else None
    jobs    = JobPosting.objects.filter(active=True)
    return render(request, 'alumni/dashboard.html', {'profile': profile, 'jobs': jobs})

@login_required
def request_mentorship(request, pk):
    mentor = get_object_or_404(AlumniProfile, pk=pk)
    member = getattr(request.user, 'member', None)
    if member:
        MentorshipMatch.objects.get_or_create(mentor=mentor, mentee=member)
        messages.success(request, 'Mentorship request sent!')
    return redirect('alumni_profile', pk=pk)
""")

w('sponsorship/views.py', """
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
""")

w('newsletter/views.py', """
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from .models import NewsletterSubscriber

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        name  = request.POST.get('name', '').strip()
        if email:
            obj, created = NewsletterSubscriber.objects.get_or_create(email=email)
            obj.name       = name or obj.name
            obj.subscribed = True
            obj.save()
            messages.success(request, 'Subscribed successfully!')
    return redirect(request.META.get('HTTP_REFERER', '/'))

def unsubscribe(request, email):
    try:
        sub = NewsletterSubscriber.objects.get(email=email)
        sub.subscribed      = False
        sub.unsubscribed_at = timezone.now()
        sub.save()
    except NewsletterSubscriber.DoesNotExist:
        pass
    return redirect('/')
""")

w('dashboard/views.py', """
import csv
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from members.models import Member
from events.models import Event, RSVP
from pages.models import ContactMessage

@staff_member_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html', {
        'total_members':   Member.objects.count(),
        'approved':        Member.objects.filter(status='approved').count(),
        'pending':         Member.objects.filter(status='pending').count(),
        'total_events':    Event.objects.count(),
        'total_rsvps':     RSVP.objects.count(),
        'unread_messages': ContactMessage.objects.filter(read=False).count(),
    })

@staff_member_required
def export_members(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="members.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name','Email','Reg No','Tier','Status','Joined','Dues Paid'])
    for m in Member.objects.select_related('user').all():
        writer.writerow([m.user.get_full_name(), m.user.email,
                         m.registration_number, m.tier, m.status,
                         m.date_joined, m.has_paid_dues])
    return response

@staff_member_required
def export_rsvps(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rsvps.csv"'
    writer = csv.writer(response)
    writer.writerow(['Event','Member','Checked In','Checked In At'])
    for r in RSVP.objects.select_related('event','member__user').all():
        writer.writerow([r.event.title, str(r.member), r.checked_in, r.checked_in_at])
    return response

@staff_member_required
def export_contacts(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name','Email','Subject','Message','Submitted','Read'])
    for c in ContactMessage.objects.all():
        writer.writerow([c.name, c.email, c.subject, c.message, c.submitted_at, c.read])
    return response
""")

w('pages/urls.py', """
from django.urls import path
from . import views
urlpatterns = [
    path('',        views.home,    name='home'),
    path('about/',  views.about,   name='about'),
    path('contact/',views.contact, name='contact'),
]
""")

w('members/urls.py', """
from django.urls import path
from . import views
urlpatterns = [
    path('login/',   views.member_login,   name='member_login'),
    path('logout/',  views.member_logout,  name='member_logout'),
    path('profile/', views.member_profile, name='member_profile'),
]
""")

w('events/urls.py', """
from django.urls import path
from . import views
urlpatterns = [
    path('',                  views.event_list,   name='event_list'),
    path('<slug:slug>/',      views.event_detail, name='event_detail'),
    path('<slug:slug>/rsvp/', views.rsvp_toggle,  name='rsvp_toggle'),
]
""")

w('news/urls.py', """
from django.urls import path
from . import views
urlpatterns = [
    path('',             views.post_list,   name='post_list'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
""")

w('resources/urls.py', """
from django.urls import path
from . import views
urlpatterns = [
    path('',           views.resource_list,   name='resource_list'),
    path('<int:pk>/',  views.resource_detail, name='resource_detail'),
]
""")

w('gallery/urls.py', """
from django.urls import path
from . import views
urlpatterns = [
    path('',          views.gallery_list,   name='gallery_list'),
    path('<int:pk>/', views.gallery_detail, name='gallery_detail'),
]
""")

w('alumni/urls.py', """
from django.urls import path
from . import views
urlpatterns = [
    path('',                             views.alumni_directory,   name='alumni_directory'),
    path('profile/<int:pk>/',            views.alumni_profile,     name='alumni_profile'),
    path('dashboard/',                   views.alumni_dashboard,   name='alumni_dashboard'),
    path('request-mentorship/<int:pk>/', views.request_mentorship, name='request_mentorship'),
]
""")

w('sponsorship/urls.py', """
from django.urls import path
from . import views
urlpatterns = [
    path('', views.sponsorship_page, name='sponsorship_page'),
]
""")

w('newsletter/urls.py', """
from django.urls import path
from . import views
urlpatterns = [
    path('subscribe/',               views.subscribe,   name='newsletter_subscribe'),
    path('unsubscribe/<str:email>/', views.unsubscribe, name='newsletter_unsubscribe'),
]
""")

w('dashboard/urls.py', """
from django.urls import path
from . import views
urlpatterns = [
    path('',                views.dashboard,       name='dashboard'),
    path('export/members/', views.export_members,  name='export_members'),
    path('export/rsvps/',   views.export_rsvps,    name='export_rsvps'),
    path('export/contacts/',views.export_contacts, name='export_contacts'),
]
""")

w('pages/admin.py', """
from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('name','email','subject','submitted_at','read')
    list_filter   = ('read',)
    list_editable = ('read',)
""")

w('members/admin.py', """
from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display  = ('user','registration_number','tier','status','has_paid_dues')
    list_filter   = ('tier','status','has_paid_dues')
    list_editable = ('status','has_paid_dues')
    search_fields = ('user__first_name','user__last_name','registration_number')
""")

w('events/admin.py', """
from django.contrib import admin
from .models import Event, RSVP

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display        = ('title','venue','start_datetime','is_outreach','capacity')
    prepopulated_fields = {'slug':('title',)}

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('event','member','checked_in','checked_in_at')
    list_filter  = ('checked_in','event')
""")

w('news/admin.py', """
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display        = ('title','category','published_at')
    list_filter         = ('category',)
    prepopulated_fields = {'slug':('title',)}
""")

w('resources/admin.py', """
from django.contrib import admin
from .models import Resource

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title','category','uploaded_at')
    list_filter  = ('category',)
""")

w('gallery/admin.py', """
from django.contrib import admin
from .models import GalleryAlbum, GalleryPhoto

admin.site.register(GalleryAlbum)
admin.site.register(GalleryPhoto)
""")

w('alumni/admin.py', """
from django.contrib import admin
from .models import AlumniProfile, MentorshipMatch, JobPosting

admin.site.register(AlumniProfile)
admin.site.register(MentorshipMatch)
admin.site.register(JobPosting)
""")

w('sponsorship/admin.py', """
from django.contrib import admin
from .models import SponsorshipTier, Sponsor, SponsorshipInquiry

admin.site.register(SponsorshipTier)
admin.site.register(Sponsor)

@admin.register(SponsorshipInquiry)
class SponsorshipInquiryAdmin(admin.ModelAdmin):
    list_display  = ('company_name','contact_name','email','responded','submitted_at')
    list_editable = ('responded',)
""")

w('newsletter/admin.py', """
from django.contrib import admin
from .models import NewsletterSubscriber, Newsletter

admin.site.register(NewsletterSubscriber)
admin.site.register(Newsletter)
""")

w('dashboard/admin.py', "")

w('templates/base.html', """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{% block title %}KAFUOSA{% endblock %}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: { extend: {
        colors: { forest:'#1a5c38', leaf:'#2d8653', gold:'#e8a020', charcoal:'#1e1e1e' },
        fontFamily: { display:['"Playfair Display"','serif'], body:['Inter','sans-serif'] }
      }}
    }
  </script>
  <style>
    body{font-family:'Inter',sans-serif;}
    .nav-link{color:white;font-size:.875rem;font-weight:500;letter-spacing:.05em;transition:color .2s;}
    .nav-link:hover{color:#e8a020;}
    .btn-primary{background:#e8a020;color:white;font-weight:600;padding:.5rem 1.5rem;border-radius:.25rem;transition:background .2s;display:inline-block;}
    .btn-primary:hover{background:#ca8a04;}
    .section-eyebrow{color:#e8a020;font-size:.75rem;font-weight:600;text-transform:uppercase;letter-spacing:.15em;}
    .section-heading{font-family:'Playfair Display',serif;color:#1e1e1e;font-size:2.25rem;font-weight:700;line-height:1.2;}
    .card{border-radius:.5rem;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.08);transition:transform .3s,box-shadow .3s;}
    .card:hover{transform:translateY(-4px);box-shadow:0 8px 24px rgba(0,0,0,.12);}
  </style>
  {% block extra_head %}{% endblock %}
</head>
<body class="bg-white text-gray-800">

<nav class="bg-[#1a5c38] sticky top-0 z-50 shadow-md">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-16">
      <a href="/" style="font-family:'Playfair Display',serif" class="text-white font-bold text-xl">
        KAF<span style="color:#e8a020">UOSA</span>
      </a>
      <div class="hidden md:flex items-center gap-8">
        <a href="/"          class="nav-link">Home</a>
        <a href="/about/"    class="nav-link">About</a>
        <a href="/events/"   class="nav-link">Events</a>
        <a href="/news/"     class="nav-link">News</a>
        <a href="/gallery/"  class="nav-link">Gallery</a>
        <a href="/alumni/"   class="nav-link">Alumni</a>
        <a href="/contact/"  class="nav-link">Contact</a>
      </div>
      <div class="hidden md:block">
        {% if user.is_authenticated %}
          <a href="/members/profile/" class="btn-primary text-sm">My Profile</a>
        {% else %}
          <a href="/members/login/"   class="btn-primary text-sm">Join / Login</a>
        {% endif %}
      </div>
      <button id="nav-toggle" class="md:hidden text-white">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
        </svg>
      </button>
    </div>
    <div id="mobile-menu" class="hidden md:hidden pb-4 space-y-2">
      <a href="/"         class="block nav-link py-1">Home</a>
      <a href="/about/"   class="block nav-link py-1">About</a>
      <a href="/events/"  class="block nav-link py-1">Events</a>
      <a href="/news/"    class="block nav-link py-1">News</a>
      <a href="/gallery/" class="block nav-link py-1">Gallery</a>
      <a href="/alumni/"  class="block nav-link py-1">Alumni</a>
      <a href="/contact/" class="block nav-link py-1">Contact</a>
      {% if user.is_authenticated %}
        <a href="/members/profile/" class="btn-primary text-sm mt-2">My Profile</a>
      {% else %}
        <a href="/members/login/"   class="btn-primary text-sm mt-2">Join / Login</a>
      {% endif %}
    </div>
  </div>
</nav>

{% if messages %}
<div class="max-w-7xl mx-auto px-4 pt-4 space-y-2">
  {% for message in messages %}
  <div class="px-4 py-3 rounded text-sm font-medium
    {% if message.tags == 'success' %}bg-green-100 text-green-800
    {% elif message.tags == 'error' %}bg-red-100 text-red-800
    {% else %}bg-blue-100 text-blue-800{% endif %}">{{ message }}</div>
  {% endfor %}
</div>
{% endif %}

<main>{% block content %}{% endblock %}</main>

<footer class="bg-[#1e1e1e] text-gray-300 pt-12 pb-6 mt-16">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-10">
      <div>
        <span style="font-family:'Playfair Display',serif" class="text-white text-2xl font-bold">
          KAF<span style="color:#e8a020">UOSA</span>
        </span>
        <p class="mt-3 text-sm text-gray-400 leading-relaxed">
          Kaimosi Friends University Optometry Students Association —
          advancing eye care education and community outreach in Kenya.
        </p>
      </div>
      <div>
        <h4 class="text-white font-semibold text-sm uppercase tracking-widest mb-4">Quick Links</h4>
        <ul class="space-y-2 text-sm">
          <li><a href="/about/"     class="hover:text-[#e8a020] transition-colors">About Us</a></li>
          <li><a href="/events/"    class="hover:text-[#e8a020] transition-colors">Events</a></li>
          <li><a href="/news/"      class="hover:text-[#e8a020] transition-colors">News</a></li>
          <li><a href="/resources/" class="hover:text-[#e8a020] transition-colors">Resources</a></li>
          <li><a href="/gallery/"   class="hover:text-[#e8a020] transition-colors">Gallery</a></li>
        </ul>
      </div>
      <div>
        <h4 class="text-white font-semibold text-sm uppercase tracking-widest mb-4">Community</h4>
        <ul class="space-y-2 text-sm">
          <li><a href="/alumni/"      class="hover:text-[#e8a020] transition-colors">Alumni Network</a></li>
          <li><a href="/sponsorship/" class="hover:text-[#e8a020] transition-colors">Sponsorship</a></li>
          <li><a href="/contact/"     class="hover:text-[#e8a020] transition-colors">Contact Us</a></li>
        </ul>
      </div>
      <div>
        <h4 class="text-white font-semibold text-sm uppercase tracking-widest mb-4">Newsletter</h4>
        <p class="text-sm text-gray-400 mb-3">Stay updated with KAFUOSA news.</p>
        <form action="/newsletter/subscribe/" method="post" class="flex gap-2">
          {% csrf_token %}
          <input type="email" name="email" placeholder="Your email"
                 class="flex-1 bg-gray-700 text-white text-sm px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-[#e8a020] placeholder-gray-500"/>
          <button type="submit" class="btn-primary text-sm px-4 py-2">Go</button>
        </form>
      </div>
    </div>
    <div class="border-t border-gray-700 pt-6 flex flex-col md:flex-row items-center justify-between gap-3 text-sm text-gray-500">
      <p>&copy; {% now "Y" %} KAFUOSA. All rights reserved.</p>
      <p>Kaimosi Friends University, Kenya</p>
    </div>
  </div>
</footer>

<script>
  document.getElementById('nav-toggle').addEventListener('click',()=>{
    document.getElementById('mobile-menu').classList.toggle('hidden');
  });
</script>
{% block extra_js %}{% endblock %}
</body>
</html>
""")

w('templates/pages/home.html', """{% extends "base.html" %}
{% block title %}Home — KAFUOSA{% endblock %}
{% block content %}

<section class="relative bg-[#1a5c38] text-white py-28 px-4 overflow-hidden">
  <div class="absolute inset-0 opacity-10 bg-[url('https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=1400')] bg-cover bg-center"></div>
  <div class="relative max-w-4xl mx-auto text-center">
    <p class="section-eyebrow text-[#e8a020] mb-3">Kaimosi Friends University</p>
    <h1 style="font-family:'Playfair Display',serif" class="text-5xl md:text-6xl font-bold leading-tight mb-6">
      Advancing Eye Care<br/>Across Kenya
    </h1>
    <p class="text-lg text-green-100 max-w-2xl mx-auto mb-8">
      KAFUOSA unites optometry students and alumni in academic excellence,
      community outreach, and professional development.
    </p>
    <div class="flex flex-wrap gap-4 justify-center">
      <a href="/events/" class="btn-primary">View Events</a>
      <a href="/about/"  class="border-2 border-white text-white px-6 py-2 rounded font-semibold hover:bg-white hover:text-[#1a5c38] transition-colors">Learn More</a>
    </div>
  </div>
</section>

<section class="bg-white border-b">
  <div class="max-w-7xl mx-auto px-4 py-10 grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
    <div>
      <p class="text-4xl font-bold text-[#1a5c38]">{{ stats.members }}+</p>
      <p class="text-sm text-gray-500 mt-1">Active Members</p>
    </div>
    <div>
      <p class="text-4xl font-bold text-[#1a5c38]">{{ stats.events }}+</p>
      <p class="text-sm text-gray-500 mt-1">Events Held</p>
    </div>
    <div>
      <p class="text-4xl font-bold text-[#1a5c38]">{{ stats.people_screened }}+</p>
      <p class="text-sm text-gray-500 mt-1">People Screened</p>
    </div>
    <div>
      <p class="text-4xl font-bold text-[#1a5c38]">{{ stats.glasses_donated }}+</p>
      <p class="text-sm text-gray-500 mt-1">Glasses Donated</p>
    </div>
  </div>
</section>

{% if upcoming %}
<section class="max-w-7xl mx-auto px-4 py-16">
  <p class="section-eyebrow mb-2">What's On</p>
  <h2 class="section-heading mb-10">Upcoming Events</h2>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    {% for event in upcoming %}
    <a href="/events/{{ event.slug }}/" class="card block bg-white border">
      {% if event.cover_image %}
        <img src="{{ event.cover_image.url }}" class="w-full h-48 object-cover" alt="{{ event.title }}"/>
      {% else %}
        <div class="w-full h-48 bg-[#1a5c38] flex items-center justify-center">
          <span class="text-white text-4xl">📅</span>
        </div>
      {% endif %}
      <div class="p-5">
        <span class="text-xs text-[#e8a020] font-semibold uppercase">{{ event.start_datetime|date:"d M Y" }}</span>
        <h3 class="font-bold text-lg mt-1 text-[#1e1e1e]">{{ event.title }}</h3>
        <p class="text-sm text-gray-500 mt-1">📍 {{ event.venue }}</p>
      </div>
    </a>
    {% endfor %}
  </div>
  <div class="mt-8 text-center">
    <a href="/events/" class="btn-primary">All Events</a>
  </div>
</section>
{% endif %}

{% if posts %}
<section class="bg-gray-50 py-16">
  <div class="max-w-7xl mx-auto px-4">
    <p class="section-eyebrow mb-2">Latest</p>
    <h2 class="section-heading mb-10">News &amp; Articles</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      {% for post in posts %}
      <a href="/news/{{ post.slug }}/" class="card block bg-white border">
        {% if post.cover_image %}
          <img src="{{ post.cover_image.url }}" class="w-full h-44 object-cover" alt="{{ post.title }}"/>
        {% else %}
          <div class="w-full h-44 bg-gray-200 flex items-center justify-center">
            <span class="text-gray-400 text-3xl">📰</span>
          </div>
        {% endif %}
        <div class="p-5">
          <span class="text-xs text-[#e8a020] font-semibold uppercase">{{ post.get_category_display }}</span>
          <h3 class="font-bold text-lg mt-1 text-[#1e1e1e]">{{ post.title }}</h3>
          <p class="text-sm text-gray-500 mt-2 line-clamp-2">{{ post.excerpt }}</p>
        </div>
      </a>
      {% endfor %}
    </div>
    <div class="mt-8 text-center">
      <a href="/news/" class="btn-primary">All News</a>
    </div>
  </div>
</section>
{% endif %}

<section class="bg-[#1a5c38] text-white py-16 text-center px-4">
  <h2 style="font-family:'Playfair Display',serif" class="text-3xl md:text-4xl font-bold mb-4">
    Your membership matters.
  </h2>
  <p class="text-green-100 mb-8 max-w-xl mx-auto">
    Join KAFUOSA and be part of a community driving change in eye care across Kenya.
  </p>
  <a href="/members/login/" class="btn-primary">Join Today</a>
</section>

{% endblock %}
""")

stubs = {
  'pages/about.html': ('About','<div class="max-w-4xl mx-auto px-4 py-16"><h1 class="section-heading">About KAFUOSA</h1><p class="mt-4 text-gray-600">Content coming soon.</p></div>'),
  'pages/contact.html': ('Contact Us','<div class="max-w-2xl mx-auto px-4 py-16"><h1 class="section-heading mb-8">Contact Us</h1><form method="post" class="space-y-4">{% csrf_token %}<input name="name" placeholder="Your Name" class="w-full border px-4 py-3 rounded focus:ring-2 focus:ring-[#1a5c38] focus:outline-none"/><input name="email" type="email" placeholder="Email" class="w-full border px-4 py-3 rounded focus:ring-2 focus:ring-[#1a5c38] focus:outline-none"/><input name="subject" placeholder="Subject" class="w-full border px-4 py-3 rounded focus:ring-2 focus:ring-[#1a5c38] focus:outline-none"/><textarea name="message" rows="5" placeholder="Message" class="w-full border px-4 py-3 rounded focus:ring-2 focus:ring-[#1a5c38] focus:outline-none"></textarea><button type="submit" class="btn-primary">Send Message</button></form></div>'),
  'members/login.html': ('Login','<div class="max-w-sm mx-auto px-4 py-20"><h1 class="section-heading mb-8 text-center">Member Login</h1><form method="post" class="space-y-4 bg-white border rounded-lg p-8 shadow-sm">{% csrf_token %}<input name="username" placeholder="Username" class="w-full border px-4 py-3 rounded focus:ring-2 focus:ring-[#1a5c38] focus:outline-none"/><input name="password" type="password" placeholder="Password" class="w-full border px-4 py-3 rounded focus:ring-2 focus:ring-[#1a5c38] focus:outline-none"/><button type="submit" class="btn-primary w-full text-center">Login</button></form></div>'),
  'members/profile.html': ('My Profile','<div class="max-w-2xl mx-auto px-4 py-16"><h1 class="section-heading mb-4">My Profile</h1>{% if member %}<p class="text-gray-600">Status: <strong class="text-[#1a5c38]">{{ member.get_status_display }}</strong></p><p class="text-gray-600 mt-2">Tier: {{ member.get_tier_display }}</p>{% else %}<p class="text-gray-500">No member profile linked to your account.</p>{% endif %}<a href="/members/logout/" class="btn-primary mt-8 inline-block">Logout</a></div>'),
  'events/event_list.html': ('Events','<div class="max-w-7xl mx-auto px-4 py-16"><h1 class="section-heading mb-8">Events</h1><div class="grid grid-cols-1 md:grid-cols-3 gap-6">{% for e in events %}<a href="/events/{{ e.slug }}/" class="card block bg-white border p-5"><p class="text-xs text-[#e8a020] font-semibold">{{ e.start_datetime|date:"d M Y" }}</p><h3 class="font-bold text-lg mt-1">{{ e.title }}</h3><p class="text-sm text-gray-500 mt-1">{{ e.venue }}</p></a>{% empty %}<p class="text-gray-500 col-span-3">No events yet.</p>{% endfor %}</div></div>'),
  'events/event_detail.html': ('{{ event.title }}','<div class="max-w-4xl mx-auto px-4 py-16">{% if event.cover_image %}<img src="{{ event.cover_image.url }}" class="w-full h-64 object-cover rounded-lg mb-8"/>{% endif %}<h1 class="section-heading">{{ event.title }}</h1><p class="text-gray-500 mt-2">{{ event.venue }} &mdash; {{ event.start_datetime|date:"d M Y, H:i" }}</p><div class="mt-8 prose max-w-none text-gray-700">{{ event.description }}</div>{% if user.is_authenticated %}<form method="post" action="/events/{{ event.slug }}/rsvp/">{% csrf_token %}<button type="submit" class="btn-primary mt-8">{% if user_rsvp %}Cancel RSVP{% else %}RSVP Now{% endif %}</button></form>{% endif %}</div>'),
  'news/post_list.html': ('News','<div class="max-w-7xl mx-auto px-4 py-16"><h1 class="section-heading mb-8">News</h1><div class="grid grid-cols-1 md:grid-cols-3 gap-6">{% for p in posts %}<a href="/news/{{ p.slug }}/" class="card block bg-white border"><div class="p-5"><span class="text-xs text-[#e8a020] font-semibold uppercase">{{ p.get_category_display }}</span><h3 class="font-bold text-lg mt-1">{{ p.title }}</h3><p class="text-sm text-gray-500 mt-2">{{ p.excerpt }}</p></div></a>{% empty %}<p class="text-gray-500">No posts yet.</p>{% endfor %}</div></div>'),
  'news/post_detail.html': ('{{ post.title }}','<div class="max-w-3xl mx-auto px-4 py-16">{% if post.cover_image %}<img src="{{ post.cover_image.url }}" class="w-full h-64 object-cover rounded-lg mb-8"/>{% endif %}<span class="section-eyebrow">{{ post.get_category_display }}</span><h1 class="section-heading mt-2">{{ post.title }}</h1><p class="text-gray-400 text-sm mt-2">{{ post.published_at|date:"d M Y" }}</p><div class="mt-8 prose max-w-none text-gray-700">{{ post.body }}</div></div>'),
  'resources/resource_list.html': ('Resources','<div class="max-w-7xl mx-auto px-4 py-16"><h1 class="section-heading mb-8">Resources</h1><div class="space-y-3">{% for r in resources %}<a href="/resources/{{ r.pk }}/" class="block border rounded-lg p-4 hover:border-[#1a5c38] transition-colors"><p class="font-bold text-[#1a5c38]">{{ r.title }}</p><p class="text-sm text-gray-500">{{ r.get_category_display }}</p></a>{% empty %}<p class="text-gray-500">No resources yet.</p>{% endfor %}</div></div>'),
  'resources/resource_detail.html': ('{{ resource.title }}','<div class="max-w-2xl mx-auto px-4 py-16"><h1 class="section-heading">{{ resource.title }}</h1><p class="text-gray-500 mt-2">{{ resource.description }}</p><a href="{{ resource.file.url }}" class="btn-primary mt-6">Download File</a></div>'),
  'gallery/gallery_list.html': ('Gallery','<div class="max-w-7xl mx-auto px-4 py-16"><h1 class="section-heading mb-8">Gallery</h1><div class="grid grid-cols-2 md:grid-cols-3 gap-4">{% for album in albums %}<a href="/gallery/{{ album.pk }}/" class="card block bg-white border p-4"><p class="font-bold text-[#1a5c38]">{{ album.title }}</p><p class="text-sm text-gray-500 mt-1">{{ album.photos.count }} photo{{ album.photos.count|pluralize }}</p></a>{% empty %}<p class="text-gray-500 col-span-3">No albums yet.</p>{% endfor %}</div></div>'),
  'gallery/gallery_detail.html': ('{{ album.title }}','<div class="max-w-7xl mx-auto px-4 py-16"><h1 class="section-heading mb-8">{{ album.title }}</h1><div class="grid grid-cols-2 md:grid-cols-3 gap-4">{% for photo in album.photos.all %}<div class="card"><img src="{{ photo.image.url }}" alt="{{ photo.caption }}" class="w-full h-48 object-cover"/>{% if photo.caption %}<p class="p-2 text-sm text-gray-500">{{ photo.caption }}</p>{% endif %}</div>{% endfor %}</div></div>'),
  'alumni/directory.html': ('Alumni','<div class="max-w-7xl mx-auto px-4 py-16"><h1 class="section-heading mb-8">Alumni Directory</h1><div class="grid grid-cols-1 md:grid-cols-2 gap-4">{% for p in profiles %}<a href="/alumni/profile/{{ p.pk }}/" class="card block bg-white border p-5"><p class="font-bold text-[#1a5c38]">{{ p.member }}</p><p class="text-sm text-gray-500">{{ p.job_title }}{% if p.current_employer %} at {{ p.current_employer }}{% endif %}</p><p class="text-xs text-gray-400 mt-1">Class of {{ p.graduation_year }}</p></a>{% empty %}<p class="text-gray-500">No alumni profiles yet.</p>{% endfor %}</div></div>'),
  'alumni/profile.html': ('{{ profile.member }}','<div class="max-w-2xl mx-auto px-4 py-16"><h1 class="section-heading">{{ profile.member }}</h1><p class="text-gray-500 mt-2">{{ profile.job_title }}{% if profile.current_employer %} at {{ profile.current_employer }}{% endif %}</p><p class="text-gray-400 text-sm">Class of {{ profile.graduation_year }}</p>{% if profile.bio %}<p class="mt-6 text-gray-700">{{ profile.bio }}</p>{% endif %}{% if user.is_authenticated %}<a href="/alumni/request-mentorship/{{ profile.pk }}/" class="btn-primary mt-6">Request Mentorship</a>{% endif %}</div>'),
  'alumni/dashboard.html': ('Alumni Dashboard','<div class="max-w-4xl mx-auto px-4 py-16"><h1 class="section-heading mb-8">Alumni Dashboard</h1><h2 class="font-bold text-lg mb-4 text-[#1a5c38]">Job Board</h2>{% for job in jobs %}<div class="border rounded-lg p-5 mb-3"><p class="font-bold">{{ job.title }}</p><p class="text-sm text-gray-500">{{ job.company }} &mdash; {{ job.location }}</p><a href="{{ job.application_link }}" class="text-[#e8a020] text-sm font-medium mt-2 inline-block" target="_blank">Apply Now &rarr;</a></div>{% empty %}<p class="text-gray-500">No job postings yet.</p>{% endfor %}</div>'),
  'sponsorship/sponsorship.html': ('Sponsorship','<div class="max-w-4xl mx-auto px-4 py-16"><h1 class="section-heading mb-8">Sponsorship Opportunities</h1>{% for tier in tiers %}<div class="border rounded-lg p-6 mb-4"><h2 class="font-bold text-xl text-[#1a5c38]">{{ tier.name }}</h2><p class="text-[#e8a020] font-semibold mt-1">KSh {{ tier.price }}</p><p class="text-gray-600 mt-2">{{ tier.description }}</p></div>{% endfor %}</div>'),
  'dashboard/dashboard.html': ('Staff Dashboard','<div class="max-w-7xl mx-auto px-4 py-16"><h1 class="section-heading mb-8">Staff Dashboard</h1><div class="grid grid-cols-2 md:grid-cols-3 gap-6 mb-10"><div class="bg-[#1a5c38] text-white rounded-lg p-6 text-center"><p class="text-4xl font-bold">{{ total_members }}</p><p class="text-sm mt-1 opacity-75">Total Members</p></div><div class="bg-[#2d8653] text-white rounded-lg p-6 text-center"><p class="text-4xl font-bold">{{ approved }}</p><p class="text-sm mt-1 opacity-75">Approved</p></div><div class="bg-[#e8a020] text-white rounded-lg p-6 text-center"><p class="text-4xl font-bold">{{ pending }}</p><p class="text-sm mt-1 opacity-75">Pending</p></div><div class="bg-gray-700 text-white rounded-lg p-6 text-center"><p class="text-4xl font-bold">{{ total_events }}</p><p class="text-sm mt-1 opacity-75">Events</p></div><div class="bg-gray-600 text-white rounded-lg p-6 text-center"><p class="text-4xl font-bold">{{ total_rsvps }}</p><p class="text-sm mt-1 opacity-75">RSVPs</p></div><div class="bg-red-700 text-white rounded-lg p-6 text-center"><p class="text-4xl font-bold">{{ unread_messages }}</p><p class="text-sm mt-1 opacity-75">Unread Messages</p></div></div><div class="flex gap-4 flex-wrap"><a href="/dashboard/export/members/"  class="btn-primary">Export Members CSV</a><a href="/dashboard/export/rsvps/"    class="btn-primary">Export RSVPs CSV</a><a href="/dashboard/export/contacts/" class="btn-primary">Export Contacts CSV</a></div></div>'),
}

for path, (title, body) in stubs.items():
    w(f'templates/{path}',
      '{{% extends "base.html" %}}{{% block title %}}{title}{{% endblock %}}{{% block content %}}{body}{{% endblock %}}'.format(title=title, body=body))

print()
print('ALL FILES WRITTEN.')
