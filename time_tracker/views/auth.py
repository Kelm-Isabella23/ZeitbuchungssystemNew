from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


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
