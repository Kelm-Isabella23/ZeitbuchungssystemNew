from django.contrib import messages  #Nachrichten-/Feedback-System für den Nutzer (Erfolg/Info/Fehler im UI)
from django.contrib.auth.decorators import login_required # Decorator: zwingt Login für eine View (sonst Redirect zur Login-Seite)
from django.contrib.auth.models import User # Standard-Django-User-Modell (wird hier zur Nutzerverwaltung im Admin-Panel genutzt)
from django.shortcuts import redirect, render  # Hilfsfunktionen für Django-Responses - redirect: Weiterleitung auf eine URL (per name=...)/ render: Template + Context zu einer HTML-Response
from time_tracker.decorators import require_role #Eigener Decorator für Rollenprüfung (ADMIN/VIP/USER)
from time_tracker.models import RoleRequest #Modell für Rollen-Anträge 


@login_required
def request_vip(request):

    #nur normale User dürfen VIP beantragen
    if request.user.profile.role != "USER":
        return redirect("dashboard")

    #prüft, ob bereits ein offener VIP-Antrag existiert
    if RoleRequest.objects.filter(
        user=request.user, requested_role="VIP", status="PENDING"
    ).exists():
        messages.info(request, "Du hast bereits einen offenen VIP-Antrag.")
        return redirect("dashboard")

    #legt neuen Antrag an
    RoleRequest.objects.create(user=request.user, requested_role="VIP")
    messages.success(request, "VIP-Antrag wurde gestellt.")
    return redirect("dashboard")


@login_required
def request_admin(request):
    
    #nur VIP darf Admin beantragen
    if request.user.profile.role != "VIP":
        return redirect("dashboard")

    #prüft, ob bereits ein offener Admin-Antrag existiert
    if RoleRequest.objects.filter(
        user=request.user, requested_role="ADMIN", status="PENDING"
    ).exists():
        messages.info(request, "Du hast bereits einen offenen Admin-Antrag.")
        return redirect("dashboard")

    #legt neuen Antrag an
    RoleRequest.objects.create(user=request.user, requested_role="ADMIN")
    messages.success(request, "Admin-Antrag wurde gestellt.")
    return redirect("dashboard")


@require_role("ADMIN")
def admin_requests(request):
    
    #lädt alle offenen Anträge, neueste zuerst
    pending = (
        RoleRequest.objects.filter(status="PENDING")
        .select_related("user")
        .order_by("-created_at")
    )

    #POST: Admin entscheidet über einen Antrag
    if request.method == "POST":
        req_id = request.POST.get("req_id")
        action = request.POST.get("action")

        #holt den passenden offenen Antrag (Sicherheitscheck)
        rr = (
            RoleRequest.objects.filter(id=req_id, status="PENDING")
            .select_related("user")
            .first()
        )
        if rr is None:
            return redirect("admin_requests")

        if action == "approve":
            #Antrag genehmigen
            rr.status = "APPROVED"
            rr.save()

            #Rolle im Profil des Users setzen
            profile = rr.user.profile
            profile.role = rr.requested_role
            profile.save()

            messages.success(
                request,
                f"Antrag genehmigt: {rr.user.username} ist jetzt {rr.requested_role}.",
            )

        elif action == "reject":
            #Antrag ablehnen
            rr.status = "REJECTED"
            rr.save()
            messages.info(request, f"Antrag abgelehnt: {rr.user.username}.")

        return redirect("admin_requests")

    #GET: Seite anzeigen
    return render(
        request,
        "admin_requests.html",
        {"pending": pending, "role": request.user.profile.role},
    )


@require_role("ADMIN")
def admin_users(request):
  
    #lädt alle User inkl. Profil (für role/is_blocked Anzeige)
    users = User.objects.all().select_related("profile").order_by("username")

    #POST: block/unblock Aktion auf einen User
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")

        #Sicherheitscheck: User muss existieren
        u = User.objects.filter(id=user_id).first()
        if u is None:
            return redirect("admin_users")

        #Superuser soll nicht gesperrt werden können
        if u.is_superuser:
            messages.error(request, "Superuser kann nicht gesperrt werden.")
            return redirect("admin_users")

        #Benutzer sperren oder entsperren (über Profile-Flag)
        if action == "block":
            u.profile.is_blocked = True
            u.profile.save()
        elif action == "unblock":
            u.profile.is_blocked = False
            u.profile.save()

        return redirect("admin_users")

    #GET: Seite anzeigen
    return render(
        request,
        "admin_users.html",
        {"users": users, "role": request.user.profile.role},
    )
