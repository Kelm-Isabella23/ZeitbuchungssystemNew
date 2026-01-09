from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from time_tracker.services import get_module_stats

@login_required
def print_report(request):
    rows, total_all = get_module_stats(request.user)
    return render(
        request,
        "print_report.html",
        {
            "rows": rows,
            "total_all": total_all,
            "username": request.user.username,
        },
    )
