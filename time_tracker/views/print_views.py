# Decorator: erlaubt Zugriff nur für eingeloggte Benutzer
from django.contrib.auth.decorators import login_required

# Rendert ein Template mit Kontextdaten
from django.shortcuts import render

# Service-Funktion zur Berechnung der Modul-Statistiken
# Wird für die Druckansicht wiederverwendet
from time_tracker.services import get_module_stats


@login_required
def print_report(request):
    """
    Druckansicht der Zeitstatistik eines Benutzers.

    Zeigt aggregierte Zeiten je Modul sowie
    die Gesamtarbeitszeit an.
    """
    # Holt Statistikdaten aus der Service-Schicht
    rows, total_all = get_module_stats(request.user)

    return render(
        request,
        "print_report.html",
        {
            "rows": rows,                 # Statistik je Modul
            "total_all": total_all,       # Gesamtminuten
            "username": request.user.username,
        },
    )
