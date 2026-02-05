"""
Zentrale URL-Konfigurationsdatei des Django-Projekts.

Definiert, welche URLs existieren und
an welche App oder View die Anfragen weitergeleitet werden.
"""

# Stellt das Django-Admin-Interface bereit
from django.contrib import admin

# Funktionen zur Definition von URL-Pfaden
# path: einzelne URL-Routen
# include: Einbindung von URLs aus anderen Apps
from django.urls import path, include


# Liste aller URL-Routen des Projekts
urlpatterns = [
    # URL für das Django-Admin-Backend
    path('admin/', admin.site.urls),

    # Übergibt alle übrigen URLs an die time_tracker-App
    path("", include("time_tracker.urls")),
]
