from django.contrib.auth.decorators import login_required #Decorator: erlaubt Zugriff nur für eingeloggte Benutzer
from django.shortcuts import render  #Rendert ein Template mit Kontextdaten
from time_tracker.services import get_module_stats #Service-Funktion zur Berechnung der Modul-StatistikenvWird für die Druckansicht wiederverwendet


@login_required
def print_report(request):
    """
    Druckansicht der Zeitstatistik eines Benutzers
    (Zeigt aggregierte Zeiten je Modul sowie die Gesamtarbeitszeit an)
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
