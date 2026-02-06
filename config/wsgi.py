"""
WSGI-Konfigurationsdatei des Django-Projekts
(Stellt den Einstiegspunkt für klassische, synchrone Webserver bereit)
"""

import os  # Zugriff auf Betriebssystem-Funktionen zum Setzen von Umgebungsvariablen
from django.core.wsgi import get_wsgi_application # Django-Funktion zum Erzeugen der WSGI-Anwendung/ Bindet das Django-Projekt an einen WSGI-Server


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Legt fest, welche Settings-Datei Django verwenden soll (hier: config/settings.py)

application = get_wsgi_application() # Erstellt die WSGI-Anwendung, die vom Webserver geladen wird
