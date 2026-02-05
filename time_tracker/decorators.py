# Stellt Hilfsfunktionen bereit, um Funktionen mit Metadaten zu umhüllen
# Wird hier verwendet, um View-Funktionen korrekt zu dekorieren
from functools import wraps

# Ermöglicht Weiterleitungen zu anderen Views anhand ihres Namens
from django.shortcuts import redirect


def require_role(*roles):
    """
    Decorator zur Zugriffsbeschränkung von Views.

    Erlaubt den Zugriff nur für angemeldete Benutzer
    mit einer bestimmten Rolle.
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Prüft, ob der Benutzer angemeldet ist
            if not request.user.is_authenticated:
                return redirect("login")

            # Zugriff auf das zugehörige Benutzerprofil
            profile = getattr(request.user, "profile", None)

            # Prüft, ob ein Profil existiert und die Rolle erlaubt ist
            if profile is None or profile.role not in roles:
                return redirect("dashboard")

            # Führt die eigentliche View-Funktion aus
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
