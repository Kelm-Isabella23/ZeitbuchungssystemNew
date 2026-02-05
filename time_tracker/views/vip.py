# Nachrichtensystem für Benutzerfeedback (Erfolg / Fehler)
from django.contrib import messages

# HTTP-Response-Klasse zur Rückgabe von Dateien (Download)
from django.http import HttpResponse

# Weiterleitung auf andere Views per URL-Name
from django.shortcuts import redirect

# Eigener Decorator zur Rollenprüfung (nur VIP und ADMIN erlaubt)
from time_tracker.decorators import require_role

# Service-Funktionen für Import und Export von Reports
from time_tracker.services import export_reports, import_reports_overwrite


@require_role("VIP", "ADMIN")
def vip_export(request):
    """
    Exportiert Zeitbuchungen des Benutzers in ein bestimmtes Format
    (json, csv oder xml) und liefert die Datei als Download aus.
    """
    # Gewünschtes Exportformat aus der URL lesen (Standard: json)
    fmt = request.GET.get("format", "json")

    try:
        # Erzeugt den Exportinhalt über die Service-Schicht
        content = export_reports(request.user, fmt)
    except ValueError:
        # Ungültiges Format → zurück zum Dashboard
        return redirect("dashboard")

    # Erstellt eine HTTP-Antwort mit Dateidownload
    response = HttpResponse(content, content_type="text/plain")
    response["Content-Disposition"] = f'attachment; filename="reports.{fmt}"'
    return response


@require_role("VIP", "ADMIN")
def vip_import(request):
    """
    Importiert Zeitbuchungen aus einer hochgeladenen Datei
    und überschreibt bestehende Reports des Benutzers.
    """
    if request.method == "POST":
        fmt = request.POST.get("format")
        file = request.FILES.get("file")

        # Prüft, ob Datei und Format angegeben wurden
        if not file or not fmt:
            messages.error(request, "Bitte Datei und Format angeben.")
            return redirect("dashboard")

        # Dateiinhalt lesen (UTF-8-kodiert)
        content = file.read().decode("utf-8")

        try:
            # Importlogik über Service-Schicht ausführen
            import_reports_overwrite(request.user, fmt, content)
            messages.success(
                request,
                "Daten erfolgreich importiert (überschrieben)."
            )
        except Exception:
            # Allgemeiner Fehlerfang für fehlerhafte Dateien/Formate
            messages.error(
                request,
                "Fehler beim Import der Datei."
            )

        return redirect("dashboard")

    # GET-Requests werden nicht unterstützt
    return redirect("dashboard")
