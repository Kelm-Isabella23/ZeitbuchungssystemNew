from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from time_tracker.services import get_module_stats

@login_required
def dashboard(request):
    rows, total_all = get_module_stats(request.user)
    return render(
        request,
        "dashboard.html",
        {
            "rows": rows,
            "total_all": total_all,
            "role": request.user.profile.role,
        },
    )
