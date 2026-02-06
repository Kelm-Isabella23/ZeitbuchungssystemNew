from datetime import date  # Stellt Datum-/Zeitfunktionen bereit (Wird genutzt, um im Formular standardmäßig das heutige Datum zu setzen)
from django.contrib import messages  #Nachrichtensystem für Feedback im Frontend
from django.contrib.auth.decorators import login_required  #Decorator: Zugriff nur für eingeloggte Nutzer
from django.shortcuts import get_object_or_404, redirect, render #Hilfsfunktionen für typische Django-Responses
from time_tracker.models import Report  # Importiert das Report-Modell (Kernobjekt dieser Views)
from time_tracker.forms import ReportForm #Formular zur Erstellung und Bearbeitung von Reports


@login_required
def reports_list(request):
    """
    Listet alle Zeitbuchungen (Reports) des eingeloggten Nutzers auf
    """
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
    """
    Erstellt eine neue Zeitbuchung
    """
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
        {
            "template": "report_form.html",
            "context": {
                "form": form,
                "mode": "new",
                "role": request.user.profile.role,
            },
        }["template"],
        {
            "form": form,
            "mode": "new",
            "role": request.user.profile.role,
        },
    )


@login_required
def report_edit(request, report_id: int):
    """
    Bearbeitet eine bestehende Zeitbuchung des eingeloggten Nutzers
    """
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
    """
    Löscht eine Zeitbuchung (nur per POST)
    """
    if request.method == "POST":
        Report.objects.filter(id=report_id, user=request.user).delete()

    return redirect("reports_list")
