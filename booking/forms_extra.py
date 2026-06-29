from django import forms
from .models import UserProfile

class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_type', 'bio', 'hourly_rate', 'resume', 'skills', 'experience_years', 'portfolio_link']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_type'].widget = forms.Select(choices=[
            ('worker', 'Freelancer / Worker'),
            ('client', 'Client / Employer')
        ])
        for field_name, field in self.fields.items():
            if field_name != 'user_type':
                field.required = False
