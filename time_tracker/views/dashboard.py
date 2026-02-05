# Decorator: Zugriff nur für eingeloggte Benutzer
from django.contrib.auth.decorators import login_required

# Rendert ein Template mit Kontextdaten
from django.shortcuts import render

# Service-Funktion zur Berechnung von Modul-Statistiken
# Liefert Minuten je Modul + Gesamtminuten
from time_tracker.services import get_module_stats


@login_required
def dashboard(request):
    """
    Dashboard-Ansicht für eingeloggte Benutzer.

    Zeigt eine statistische Übersicht der erfassten Zeiten
    (Minuten pro Modul und Gesamtaufwand).
    """
    # Holt aggregierte Statistikdaten aus der Service-Schicht
    rows, total_all = get_module_stats(request.user)

    return render(
        request,
        "dashboard.html",
        {
            "rows": rows,               # Statistik je Modul
            "total_all": total_all,     # Gesamtminuten
            "role": request.user.profile.role,
        },
    )
