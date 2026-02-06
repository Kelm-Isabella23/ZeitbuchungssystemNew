from functools import wraps #Stellt Hilfsfunktionen bereit, um Funktionen mit Metadaten zu umhüllen (wird hier verwendet, um View-Funktionen korrekt zu dekorieren)
from django.shortcuts import redirect  # Ermöglicht Weiterleitungen zu anderen Views anhand ihres Namens


def require_role(*roles):
    """
    Erlaubt den Zugriff nur für angemeldete Benutzer mit einer bestimmten Rolle
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            
            if not request.user.is_authenticated: #Prüft, ob der Benutzer angemeldet ist
                return redirect("login") 

            #Zugriff auf das zugehörige Benutzerprofil:
            profile = getattr(request.user, "profile", None)

            if profile is None or profile.role not in roles: #Prüft, ob ein Profil existiert und die Rolle erlaubt ist
                return redirect("dashboard")

            #Führt die eigentliche View-Funktion aus:
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
