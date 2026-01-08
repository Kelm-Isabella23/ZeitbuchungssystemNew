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
