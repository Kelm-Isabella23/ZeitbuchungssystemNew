from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect

from time_tracker.decorators import require_role
from time_tracker.services import export_reports, import_reports_overwrite


@require_role("VIP", "ADMIN")
def vip_export(request):
    fmt = request.GET.get("format", "json")

    try:
        content = export_reports(request.user, fmt)
    except ValueError:
        return redirect("dashboard")

    response = HttpResponse(content, content_type="text/plain")
    response["Content-Disposition"] = f'attachment; filename="reports.{fmt}"'
    return response


@require_role("VIP", "ADMIN")
def vip_import(request):
    if request.method == "POST":
        fmt = request.POST.get("format")
        file = request.FILES.get("file")

        if not file or not fmt:
            messages.error(request, "Bitte Datei und Format angeben.")
            return redirect("dashboard")

        content = file.read().decode("utf-8")
        try:
            import_reports_overwrite(request.user, fmt, content)
            messages.success(request, "Daten erfolgreich importiert (überschrieben).")
        except Exception:
            messages.error(request, "Fehler beim Import der Datei.")

        return redirect("dashboard")

    return redirect("dashboard")
