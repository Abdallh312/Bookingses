import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import BookingSubmissionForm, UserRegistrationForm
from .forms_extra import CompleteProfileForm
from .models import PortfolioItem, Service, UserProfile, ClientBooking

logger = logging.getLogger(__name__)

def home(request):
    """
    Marketplace landing page showing top workers.
    """
    # Only show APPROVED workers on the homepage
    workers = UserProfile.objects.filter(user_type='worker', approval_status='approved').select_related('user')[:6]
    return render(request, 'booking/home.html', {'workers': workers})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            
            user_type = form.cleaned_data['user_type']
            approval_status = 'pending' if user_type == 'worker' else 'approved'
            
            UserProfile.objects.create(
                user=user,
                user_type=user_type,
                approval_status=approval_status,
                bio=form.cleaned_data.get('bio', ''),
                hourly_rate=form.cleaned_data.get('hourly_rate', None),
                resume=form.cleaned_data.get('resume'),
                skills=form.cleaned_data.get('skills', ''),
                experience_years=form.cleaned_data.get('experience_years', 0),
                portfolio_link=form.cleaned_data.get('portfolio_link', '')
            )
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'booking/register.html', {'form': form})

@login_required
def complete_profile(request):
    """
    Forces users who just signed up via Social Login to complete their profile
    by selecting if they are a Worker or a Client.
    """
    if hasattr(request.user, 'profile'):
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CompleteProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            approval_status = 'pending' if user_type == 'worker' else 'approved'
            
            UserProfile.objects.create(
                user=request.user,
                user_type=user_type,
                approval_status=approval_status,
                bio=form.cleaned_data.get('bio', ''),
                hourly_rate=form.cleaned_data.get('hourly_rate', None),
                resume=form.cleaned_data.get('resume'),
                skills=form.cleaned_data.get('skills', ''),
                experience_years=form.cleaned_data.get('experience_years', 0),
                portfolio_link=form.cleaned_data.get('portfolio_link', '')
            )
            messages.success(request, "Your profile is complete!")
            return redirect('dashboard')
    else:
        form = CompleteProfileForm()
        
    return render(request, 'booking/complete_profile.html', {'form': form})

@login_required
def dashboard(request):
    """
    Routes to the correct dashboard based on user type.
    """
    profile = request.user.profile
    if profile.user_type == 'worker':
        return render(request, 'booking/worker_dashboard.html', {
            'bookings': request.user.worker_bookings.all().order_by('-created_at')
        })
    else:
        return render(request, 'booking/client_dashboard.html', {
            'bookings': request.user.client_bookings.all().order_by('-created_at')
        })

def workers_list(request):
    """Browse all workers in the marketplace."""
    workers = UserProfile.objects.filter(user_type='worker', approval_status='approved').select_related('user')
    return render(request, 'booking/workers_list.html', {'workers': workers})

@login_required
def worker_profile(request, username):
    """
    View a specific worker's profile, their portfolio, and submit a booking.
    """
    worker_user = get_object_or_404(User, username=username, profile__user_type='worker')
    
    # Hide unapproved workers unless they are viewing their own profile
    if worker_user.profile.approval_status != 'approved' and request.user != worker_user:
        messages.error(request, "This worker profile is not currently active.")
        return redirect('workers_list')
        
    portfolio_items = worker_user.portfolio_items.all().order_by('-created_at')
    services = worker_user.services.filter(is_active=True)

    if request.method == 'POST':
        if request.user.profile.user_type == 'worker':
            messages.error(request, "Workers cannot book other workers.")
            return redirect('worker_profile', username=username)

        form = BookingSubmissionForm(request.POST)
        # We need to hack the form queryset since it's dynamic
        form.fields['services'].queryset = services
        
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            booking.worker = worker_user
            booking.save()
            form.save_m2m() # Save the many-to-many services
            
            # Send Email
            context = {
                'client_name': request.user.username,
                'worker_name': worker_user.username,
                'services': booking.services.all(),
                'preferred_date': booking.preferred_date,
                'booking_reference': f"BKG-{booking.id:04d}",
            }
            html_message = render_to_string('emails/booking_confirmation.html', context)
            send_mail(
                subject='New Booking Request!',
                message=strip_tags(html_message),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[worker_user.email, request.user.email], # Notify both
                html_message=html_message,
                fail_silently=True,
            )
            messages.success(request, "Your booking request has been sent to the worker!")
            return redirect('booking_success')
    else:
        form = BookingSubmissionForm()
        form.fields['services'].queryset = services

    context = {
        'worker_user': worker_user,
        'portfolio_items': portfolio_items,
        'services': services,
        'form': form
    }
    return render(request, 'booking/worker_profile.html', context)

def booking_success(request):
    return render(request, 'booking/success.html')
