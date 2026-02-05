from django.contrib import messages #Nachrichtensystem für Benutzerfeedback (Fehler-/Info-Meldungen im UI)
from django.contrib.auth import authenticate, login, logout  #Authentifizierungsfunktionen - authenticate: prüft Benutzername/Passwort, login: meldet Benutzer an, logout: meldet Benutzer ab
from django.contrib.auth.models import User # Standard-Django-User-Modell (Registrierung und Existenzprüfung)
from django.shortcuts import redirect, render  #Hilfsfunktionen für Responses- redirect: Weiterleitung auf eine URL, render: Template + Context zurückgeben


def home(request):
    """
    Startseite der Anwendung.

    Leitet eingeloggte Nutzer direkt zum Dashboard weiter,
    ansonsten zur Login-Seite.
    """
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


def register_view(request):
    """
    Registriert einen neuen Benutzer.

    Erstellt einen User, meldet ihn direkt an
    und leitet zum Dashboard weiter.
    """
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        # Pflichtfelder prüfen
        if not username or not password:
            messages.error(request, "Bitte Benutzername und Passwort eingeben.")
            return redirect("register")

        # Benutzername darf nur einmal existieren
        if User.objects.filter(username=username).exists():
            messages.error(request, "Benutzername ist bereits vergeben.")
            return redirect("register")

        # Benutzer anlegen und direkt einloggen
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("dashboard")

    return render(request, "register.html")


def login_view(request):
    """
    Login-Funktion für bestehende Benutzer.
    """
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        # Zugangsdaten prüfen
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(
                request,
                "Login fehlgeschlagen. Benutzername/Passwort prüfen."
            )
            return redirect("login")

        # Prüft, ob der Benutzer gesperrt ist
        if hasattr(user, "profile") and user.profile.is_blocked:
            messages.error(request, "Dein Account ist gesperrt.")
            return redirect("login")

        login(request, user)
        return redirect("dashboard")

    return render(request, "login.html")


def logout_view(request):
    """
    Meldet den Benutzer ab und leitet zur Login-Seite weiter.
    """
    logout(request)
    return redirect("login")
