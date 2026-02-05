#!/usr/bin/env python
"""
Startpunkt für alle Django-Verwaltungsbefehle.
Wird u. a. für runserver, migrate oder createsuperuser genutzt.
"""

# Zugriff auf Betriebssystem-Funktionen (z. B. Umgebungsvariablen)
import os

# Zugriff auf Kommandozeilenargumente (z. B. runserver, migrate)
import sys


def main():
    """
    Setzt die Django-Settings und leitet
    Kommandozeilenbefehle an Django weiter.
    """

    # Definiert, welche Settings-Datei Django verwenden soll
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    try:
        # Zentrale Django-Funktion zur Verarbeitung von CLI-Befehlen
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Fehlerfall: Django ist nicht installiert oder das virtuelle Umfeld ist nicht aktiv
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Übergibt die Kommandozeilenargumente an Django
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Startet die Anwendung bei direktem Aufruf der Datei
    main()
