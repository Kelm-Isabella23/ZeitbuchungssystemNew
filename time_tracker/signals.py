# Stellt Zugriff auf das aktuell konfigurierte User-Modell bereit
# Ermöglicht Kompatibilität mit benutzerdefinierten User-Modellen
from django.contrib.auth import get_user_model

# Signal, das nach dem Speichern eines Modells ausgelöst wird
from django.db.models.signals import post_save

# Dekorator zur Registrierung von Signal-Empfängern
from django.dispatch import receiver

# Importiert das Profile-Modell zur automatischen Profilerstellung
from .models import Profile


# Ermittelt das im Projekt verwendete User-Modell
User = get_user_model()


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    """
    Erstellt automatisch ein Profil für neu angelegte Benutzer.

    Wird ausgelöst, sobald ein User-Objekt gespeichert wurde.
    """
    # Nur bei neu erstellten Benutzern ausführen
    if created:
        Profile.objects.get_or_create(user=instance)
