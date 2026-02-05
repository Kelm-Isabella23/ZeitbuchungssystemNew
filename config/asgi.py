"""
ASGI-Konfigurationsdatei des Django-Projekts.

Stellt den Einstiegspunkt für ASGI-kompatible Server bereit
(z. B. für asynchrone Anwendungen, WebSockets oder moderne Deployments).
"""

import os  # Zugriff auf Betriebssystem-Funktionen zum Setzen von Umgebungsvariablen
from django.core.asgi import get_asgi_application  # Django-Funktion zum Erzeugen der ASGI-Anwendung/ Bindet das Django-Projekt an einen ASGI-Server


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') # Legt fest, welche Settings-Datei Django verwenden soll

application = get_asgi_application()# Erstellt die ASGI-Anwendung, die vom Server geladen wird
