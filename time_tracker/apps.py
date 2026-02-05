# Basisklasse für Django-App-Konfigurationen
# Wird verwendet, um Metadaten und Initialisierungslogik einer App zu definieren
from django.apps import AppConfig


class TimeTrackerConfig(AppConfig):
    """
    Konfigurationsklasse für die time_tracker-App.

    Legt grundlegende App-Eigenschaften fest
    und wird beim Start des Django-Projekts geladen.
    """

    # Standardtyp für automatisch erzeugte Primärschlüssel
    default_auto_field = "django.db.models.BigAutoField"

    # Interner Name der App (muss mit dem App-Verzeichnis übereinstimmen)
    name = "time_tracker"

    def ready(self):
        """
        Wird beim Start der App automatisch ausgeführt.

        Eignet sich zum Initialisieren von appweiten
        Funktionen wie Signalen.
        """

        # Importiert die Signal-Definitionen,
        # damit diese beim Start der App registriert werden
        import time_tracker.signals
