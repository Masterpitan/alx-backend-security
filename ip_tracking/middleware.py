import datetime
from .models import RequestLog

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get client IP
        ip = self.get_client_ip(request)
        # Get path
        path = request.path
        # Save request log
        RequestLog.objects.create(
            ip_address=ip,
            path=path,
            timestamp=datetime.datetime.now()
        )
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Retrieve the client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
