from django import forms
from django.utils import timezone
from .models import ClientBooking, Service

class BookingSubmissionForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple
    )
    
    class Meta:
        model = ClientBooking
        fields = ['services', 'preferred_date', 'special_requests']

    def clean_preferred_date(self):
        """Ensure the client doesn't book a date in the past."""
        date = self.cleaned_data.get('preferred_date')
        if date and date < timezone.now().date():
            raise forms.ValidationError("Preferred date cannot be in the past.")
        return date

class UserRegistrationForm(forms.Form):
    USER_TYPES = [
        ('worker', 'Freelancer / Worker'),
        ('client', 'Client / Employer'),
    ]
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=USER_TYPES)
    
    # Professional fields (Optional initially, enforced later via JS)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    hourly_rate = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    resume = forms.FileField(required=False, help_text="Upload your CV (PDF or DOCX)")
    skills = forms.CharField(required=False, help_text="e.g. Python, Design, SEO")
    experience_years = forms.IntegerField(required=False, initial=0)
    portfolio_link = forms.URLField(required=False)
