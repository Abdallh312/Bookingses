from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    """
    Ensures that any user authenticated via social login completes their profile.
    If they don't have a UserProfile, redirect them to the complete_profile view.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not hasattr(request.user, 'profile'):
            # Only redirect if they are not already on the complete_profile page
            # or on a logout/static path
            if not request.path.startswith('/complete-profile/') and not request.path.startswith('/logout/') and not request.path.startswith('/admin/'):
                return redirect('complete_profile')
        
        response = self.get_response(request)
        return response
