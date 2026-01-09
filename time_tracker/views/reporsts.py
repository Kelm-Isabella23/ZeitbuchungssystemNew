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
    modules = Module.objects.filter(is_active=True).order_by("name")

    if request.method == "POST":
        date_str = request.POST.get("date", "").strip()
        minutes_str = request.POST.get("minutes", "").strip()
        module_id = request.POST.get("module_id", "").strip()
        text = request.POST.get("text", "").strip()

        if not date_str or not minutes_str or not module_id or not text:
            messages.error(request, "Bitte alle Felder ausfüllen.")
            return render(
                request,
                "report_form.html",
                {"modules": modules, "mode": "new", "role": request.user.profile.role},
            )

        try:
            minutes = int(minutes_str)
            if minutes <= 0:
                raise ValueError()
        except ValueError:
            messages.error(request, "Minuten müssen eine positive Zahl sein.")
            return render(
                request,
                "report_form.html",
                {"modules": modules, "mode": "new", "role": request.user.profile.role},
            )

        module = Module.objects.filter(id=module_id, is_active=True).first()
        if module is None:
            messages.error(request, "Ungültiges Modul.")
            return render(
                request,
                "report_form.html",
                {"modules": modules, "mode": "new", "role": request.user.profile.role},
            )

        Report.objects.create(
            user=request.user,
            date=date_str,
            minutes=minutes,
            module=module,
            text=text[:300],
        )
        return redirect("reports_list")

    return render(
        request,
        "report_form.html",
        {
            "modules": modules,
            "mode": "new",
            "today": date.today().isoformat(),
            "role": request.user.profile.role,
        },
    )


@login_required
def report_edit(request, report_id: int):
    report = get_object_or_404(Report.objects.select_related("module"), id=report_id, user=request.user)
    modules = Module.objects.filter(is_active=True).order_by("name")

    if request.method == "POST":
        date_str = request.POST.get("date", "").strip()
        minutes_str = request.POST.get("minutes", "").strip()
        module_id = request.POST.get("module_id", "").strip()
        text = request.POST.get("text", "").strip()

        if not date_str or not minutes_str or not module_id or not text:
            messages.error(request, "Bitte alle Felder ausfüllen.")
            return render(
                request,
                "report_form.html",
                {
                    "modules": modules,
                    "mode": "edit",
                    "report": report,
                    "role": request.user.profile.role,
                },
            )

        try:
            minutes = int(minutes_str)
            if minutes <= 0:
                raise ValueError()
        except ValueError:
            messages.error(request, "Minuten müssen eine positive Zahl sein.")
            return render(
                request,
                "report_form.html",
                {
                    "modules": modules,
                    "mode": "edit",
                    "report": report,
                    "role": request.user.profile.role,
                },
            )

        module = Module.objects.filter(id=module_id, is_active=True).first()
        if module is None:
            messages.error(request, "Ungültiges Modul.")
            return render(
                request,
                "report_form.html",
                {
                    "modules": modules,
                    "mode": "edit",
                    "report": report,
                    "role": request.user.profile.role,
                },
            )

        report.date = date_str
        report.minutes = minutes
        report.module = module
        report.text = text[:300]
        report.save()
        return redirect("reports_list")

    return render(
        request,
        "report_form.html",
        {"modules": modules, "mode": "edit", "report": report, "role": request.user.profile.role},
    )


@login_required
def report_delete(request, report_id: int):
    if request.method == "POST":
        Report.objects.filter(id=report_id, user=request.user).delete()
    return redirect("reports_list")
