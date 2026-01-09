from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import redirect, render

from .models import Report



def home(request):
    # Startseite: direkt ins Dashboard (oder Login, wenn nicht eingeloggt)
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            messages.error(request, "Bitte Benutzername und Passwort eingeben.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Benutzername ist bereits vergeben.")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        # Profile wird automatisch via Signal erstellt ✅
        login(request, user)
        return redirect("dashboard")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Login fehlgeschlagen. Benutzername/Passwort prüfen.")
            return redirect("login")

        # Block-Check
        if hasattr(user, "profile") and user.profile.is_blocked:
            messages.error(request, "Dein Account ist gesperrt.")
            return redirect("login")

        login(request, user)
        return redirect("dashboard")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    # Statistik: Minuten je Modul + Prozentanteil
    qs = (
        Report.objects.filter(user=request.user)
        .values("module__name")
        .annotate(total_minutes=Sum("minutes"))
        .order_by("module__name")
    )

    total_all = sum(item["total_minutes"] or 0 for item in qs) or 0

    rows = []
    for item in qs:
        minutes = item["total_minutes"] or 0
        percent = round((minutes / total_all) * 100, 1) if total_all > 0 else 0.0
        rows.append(
            {"module": item["module__name"], "minutes": minutes, "percent": percent}
        )

    return render(
        request,
        "dashboard.html",
        {
            "rows": rows,
            "total_all": total_all,
            "role": request.user.profile.role if hasattr(request.user, "profile") else "USER",
        },
    )

from datetime import date
from .models import Report, Module

@login_required
def reports_list(request):
    reports = (
        Report.objects.filter(user=request.user)
        .select_related("module")
        .order_by("-date", "-created_at")
    )
    return render(request, "reports_list.html", {"reports": reports, "role": request.user.profile.role})


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
            return render(request, "report_form.html", {
                "modules": modules,
                "mode": "new",
                "role": request.user.profile.role,
            })

        try:
            minutes = int(minutes_str)
            if minutes <= 0:
                raise ValueError()
        except ValueError:
            messages.error(request, "Minuten müssen eine positive Zahl sein.")
            return render(request, "report_form.html", {
                "modules": modules,
                "mode": "new",
                "role": request.user.profile.role,
            })

        # Modul prüfen (nur aktive Module erlauben)
        try:
            module = Module.objects.get(id=module_id, is_active=True)
        except Module.DoesNotExist:
            messages.error(request, "Ungültiges Modul.")
            return render(request, "report_form.html", {
                "modules": modules,
                "mode": "new",
                "role": request.user.profile.role,
            })

        Report.objects.create(
            user=request.user,
            date=date_str,
            minutes=minutes,
            module=module,
            text=text[:300],
        )
        return redirect("reports_list")

    return render(request, "report_form.html", {
        "modules": modules,
        "mode": "new",
        "today": date.today().isoformat(),
        "role": request.user.profile.role,
    })


@login_required
def report_edit(request, report_id: int):
    try:
        report = Report.objects.select_related("module").get(id=report_id, user=request.user)
    except Report.DoesNotExist:
        return redirect("reports_list")

    modules = Module.objects.filter(is_active=True).order_by("name")

    if request.method == "POST":
        date_str = request.POST.get("date", "").strip()
        minutes_str = request.POST.get("minutes", "").strip()
        module_id = request.POST.get("module_id", "").strip()
        text = request.POST.get("text", "").strip()

        if not date_str or not minutes_str or not module_id or not text:
            messages.error(request, "Bitte alle Felder ausfüllen.")
            return render(request, "report_form.html", {
                "modules": modules,
                "mode": "edit",
                "report": report,
                "role": request.user.profile.role,
            })

        try:
            minutes = int(minutes_str)
            if minutes <= 0:
                raise ValueError()
        except ValueError:
            messages.error(request, "Minuten müssen eine positive Zahl sein.")
            return render(request, "report_form.html", {
                "modules": modules,
                "mode": "edit",
                "report": report,
                "role": request.user.profile.role,
            })

        try:
            module = Module.objects.get(id=module_id, is_active=True)
        except Module.DoesNotExist:
            messages.error(request, "Ungültiges Modul.")
            return render(request, "report_form.html", {
                "modules": modules,
                "mode": "edit",
                "report": report,
                "role": request.user.profile.role,
            })

        report.date = date_str
        report.minutes = minutes
        report.module = module
        report.text = text[:300]
        report.save()

        return redirect("reports_list")

    return render(request, "report_form.html", {
        "modules": modules,
        "mode": "edit",
        "report": report,
        "role": request.user.profile.role,
    })


@login_required
def report_delete(request, report_id: int):
    if request.method == "POST":
        Report.objects.filter(id=report_id, user=request.user).delete()
    return redirect("reports_list")


from .models import RoleRequest, Profile
from django.contrib.auth.models import User

def require_role(*roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            if request.user.profile.role not in roles:
                return redirect("dashboard")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


@login_required
def request_vip(request):
    # nur USER darf VIP beantragen
    if request.user.profile.role != "USER":
        return redirect("dashboard")

    # bereits offen?
    if RoleRequest.objects.filter(user=request.user, requested_role="VIP", status="PENDING").exists():
        messages.info(request, "Du hast bereits einen offenen VIP-Antrag.")
        return redirect("dashboard")

    RoleRequest.objects.create(user=request.user, requested_role="VIP")
    messages.success(request, "VIP-Antrag wurde gestellt.")
    return redirect("dashboard")


@login_required
def request_admin(request):
    # nur VIP darf ADMIN beantragen
    if request.user.profile.role != "VIP":
        return redirect("dashboard")

    if RoleRequest.objects.filter(user=request.user, requested_role="ADMIN", status="PENDING").exists():
        messages.info(request, "Du hast bereits einen offenen Admin-Antrag.")
        return redirect("dashboard")

    RoleRequest.objects.create(user=request.user, requested_role="ADMIN")
    messages.success(request, "Admin-Antrag wurde gestellt.")
    return redirect("dashboard")


@require_role("ADMIN")
def admin_requests(request):
    pending = RoleRequest.objects.filter(status="PENDING").select_related("user").order_by("-created_at")

    if request.method == "POST":
        req_id = request.POST.get("req_id")
        action = request.POST.get("action")  # approve / reject

        try:
            rr = RoleRequest.objects.select_related("user").get(id=req_id, status="PENDING")
        except RoleRequest.DoesNotExist:
            return redirect("admin_requests")

        if action == "approve":
            rr.status = "APPROVED"
            rr.save()

            # Rolle setzen
            profile = rr.user.profile
            profile.role = rr.requested_role
            profile.save()

            messages.success(request, f"Antrag genehmigt: {rr.user.username} ist jetzt {rr.requested_role}.")
        elif action == "reject":
            rr.status = "REJECTED"
            rr.save()
            messages.info(request, f"Antrag abgelehnt: {rr.user.username}.")
        return redirect("admin_requests")

    return render(request, "admin_requests.html", {"pending": pending, "role": request.user.profile.role})


@require_role("ADMIN")
def admin_users(request):
    users = User.objects.all().select_related("profile").order_by("username")

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")  # block / unblock

        try:
            u = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect("admin_users")

        if u.is_superuser:
            messages.error(request, "Superuser kann nicht gesperrt werden.")
            return redirect("admin_users")

        if action == "block":
            u.profile.is_blocked = True
            u.profile.save()
        elif action == "unblock":
            u.profile.is_blocked = False
            u.profile.save()

        return redirect("admin_users")

    return render(request, "admin_users.html", {"users": users, "role": request.user.profile.role})


from django.http import HttpResponse
from .services import export_reports, import_reports_overwrite


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

@login_required
def print_report(request):
    # gleiche Daten wie Dashboard: Minuten je Modul + Prozent
    qs = (
        Report.objects.filter(user=request.user)
        .values("module__name")
        .annotate(total_minutes=Sum("minutes"))
        .order_by("module__name")
    )
    total_all = sum(item["total_minutes"] or 0 for item in qs) or 0

    rows = []
    for item in qs:
        minutes = item["total_minutes"] or 0
        percent = round((minutes / total_all) * 100, 1) if total_all > 0 else 0.0
        rows.append({"module": item["module__name"], "minutes": minutes, "percent": percent})

    return render(
        request,
        "print_report.html",
        {
            "rows": rows,
            "total_all": total_all,
            "username": request.user.username,
        },
    )
