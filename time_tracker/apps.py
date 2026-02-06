from django.apps import AppConfig #Basisklasse für Django-App-Konfigurationen (Wird verwendet, um Metadaten und Initialisierungslogik einer App zu definieren)


class TimeTrackerConfig(AppConfig):
    """
    Konfigurationsklasse für die time_tracker-App
    (Legt grundlegende App-Eigenschaften fest
    und wird beim Start des Django-Projekts geladen)
    """

    # Standardtyp für automatisch erzeugte Primärschlüssel
    default_auto_field = "django.db.models.BigAutoField"

    name = "time_tracker"

    def ready(self):

        import time_tracker.signals #Importiert die Signal-Definitionen, damit diese beim Start der App registriert werden
