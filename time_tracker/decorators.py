from functools import wraps
from django.shortcuts import redirect

def require_role(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            if request.user.profile.role not in roles:
                return redirect("dashboard")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
