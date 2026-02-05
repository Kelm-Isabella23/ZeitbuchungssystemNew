"""
ASGI-Konfigurationsdatei des Django-Projekts.

Stellt den Einstiegspunkt für ASGI-kompatible Server bereit
(z. B. für asynchrone Anwendungen, WebSockets oder moderne Deployments).
"""

# Zugriff auf Betriebssystem-Funktionen zum Setzen von Umgebungsvariablen
import os

# Django-Funktion zum Erzeugen der ASGI-Anwendung
# Bindet das Django-Projekt an einen ASGI-Server
from django.core.asgi import get_asgi_application


# Legt fest, welche Settings-Datei Django verwenden soll
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Erstellt die ASGI-Anwendung, die vom Server geladen wird
application = get_asgi_application()
