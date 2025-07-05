# middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (request.user.is_authenticated and 
            hasattr(request.user, 'force_password_change') and 
            request.user.force_password_change and
            request.path not in [reverse('security:change_password'), reverse('security:logout')]):
            
            return redirect('security:change_password')
        
        response = self.get_response(request)
        return response
