from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from users.models import UsersTeacher

class PrincipalAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith('/admin/') and request.user.is_authenticated and not request.user.is_staff:
            principal_profile = UsersTeacher.objects.filter(user=request.user, roles__name='PRINCIPAL').first()
            if principal_profile:
                # If the user has the PRINCIPAL role, authenticate and login them as admin
                user = request.user
                if user:
                    login(request, user)
                    return response
        
        # Check if the user is logged out from the admin panel
        if request.path == '/admin/logout/' and request.user.is_authenticated and request.user.is_staff:
            # Logout the user and redirect them to the home page
            logout(request)
            return redirect('home')  # Adjust the URL name for the home page as needed
        
        return response
