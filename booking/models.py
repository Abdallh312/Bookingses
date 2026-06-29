from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Extends the built-in Django User model to store marketplace roles and details."""
    USER_TYPES = [
        ('worker', 'Freelancer / Worker'),
        ('client', 'Client / Employer'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='client')
    approval_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Worker specific fields (can be left blank for clients)
    bio = models.TextField(blank=True, help_text=_("Tell clients about yourself"))
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # New Professional Fields
    resume = models.FileField(upload_to='cvs/', blank=True, null=True, help_text=_("Upload your CV/Resume (PDF)"))
    skills = models.TextField(blank=True, help_text=_("List your skills (e.g., Python, React, Photoshop)"))
    experience_years = models.PositiveIntegerField(default=0, help_text=_("Years of professional experience"))
    portfolio_link = models.URLField(blank=True, null=True, help_text=_("Link to your external portfolio or LinkedIn"))
    
    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"

class Service(models.Model):
    """Represents a service offered by a specific worker."""
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200, help_text=_("e.g., Web Development, Logo Design"))
    description = models.TextField()
    base_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.00)],
        help_text=_("Starting price for this service")
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.worker.username}"

class PortfolioItem(models.Model):
    """Represents a completed project in a worker's portfolio."""
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_items')
    title = models.CharField(max_length=255)
    description = models.TextField()
    services_used = models.ManyToManyField(Service, related_name="portfolio_items", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PortfolioImage(models.Model):
    portfolio_item = models.ForeignKey(PortfolioItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='portfolio/images/')
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0, help_text=_("Display order"))

    class Meta:
        ordering = ['order']

class PortfolioVideo(models.Model):
    portfolio_item = models.ForeignKey(PortfolioItem, on_delete=models.CASCADE, related_name='videos')
    video_url = models.URLField(help_text=_("Link to the video"))
    title = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

class ClientBooking(models.Model):
    """Captures a booking request from a client to a specific worker."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_bookings')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worker_bookings')
    
    services = models.ManyToManyField(Service, related_name='bookings')
    preferred_date = models.DateField(help_text=_("Preferred project start/delivery date"))
    special_requests = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking from {self.client.username} to {self.worker.username}"
