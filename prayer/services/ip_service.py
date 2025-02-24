from django.http import HttpRequest
from typing import Dict, Optional

def get_user_ip(request: HttpRequest) -> Optional[str]:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get("REMOTE_ADDR")
    return ip_address