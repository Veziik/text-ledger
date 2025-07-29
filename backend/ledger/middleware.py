from django.utils.deprecation import MiddlewareMixin

class DisableCSRFForAPI(MiddlewareMixin):
    """Disable CSRF for API endpoints - not for production!"""
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith('/api/'):
            # This is a bad practice but works for development
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None