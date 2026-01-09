from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from time_tracker.models import Module, Report


@login_required
def reports_list(request):
    reports = (
        Report.objects.filter(user=request.user)
        .select_related("module")
        .order_by("-date", "-created_at")
    )
    return render(
        request,
        "reports_list.html",
        {"reports": reports, "role": request.user.profile.role},
    )


@login_required
def report_new(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            return redirect("reports_list")

        messages.error(request, "Bitte Eingaben prüfen.")
    else:
        form = ReportForm(initial={"date": date.today()})

    return render(
        request,
        "report_form.html",
        {
            "form": form,
            "mode": "new",
            "role": request.user.profile.role,
        },
    )


@login_required
def report_edit(request, report_id: int):
    report = get_object_or_404(Report, id=report_id, user=request.user)

    if request.method == "POST":
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect("reports_list")
        messages.error(request, "Bitte Eingaben prüfen.")
    else:
        form = ReportForm(instance=report)

    return render(
        request,
        "report_form.html",
        {
            "form": form,
            "mode": "edit",
            "report": report,
            "role": request.user.profile.role,
        },
    )


@login_required
def report_delete(request, report_id: int):
    if request.method == "POST":
        Report.objects.filter(id=report_id, user=request.user).delete()
    return redirect("reports_list")
