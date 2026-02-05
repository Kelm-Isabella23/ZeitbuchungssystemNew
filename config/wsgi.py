"""
WSGI-Konfigurationsdatei des Django-Projekts.

Stellt den Einstiegspunkt für klassische,
synchrone Webserver (z. B. Gunicorn oder uWSGI) bereit.
"""

# Zugriff auf Betriebssystem-Funktionen zum Setzen von Umgebungsvariablen
import os

# Django-Funktion zum Erzeugen der WSGI-Anwendung
# Bindet das Django-Projekt an einen WSGI-Server
from django.core.wsgi import get_wsgi_application


# Legt fest, welche Settings-Datei Django verwenden soll
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Erstellt die WSGI-Anwendung, die vom Webserver geladen wird
application = get_wsgi_application()
