from functools import wraps
from urllib.parse import urlencode
from django.conf import settings
from django.shortcuts import redirect

def model_login_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = getattr(settings, "LOGIN_URL", "/accounts/login/")
            query = urlencode({"next": request.get_full_path(), "required": "1"})
            return redirect(f"{login_url}?{query}")
        return view_func(request, *args, **kwargs)
    return _wrapped