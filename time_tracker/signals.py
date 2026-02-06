from django.contrib.auth import get_user_model  #Stellt Zugriff auf das aktuell konfigurierte User-Modell bereit und ermöglicht Kompatibilität mit benutzerdefinierten User-Modellen
from django.db.models.signals import post_save  #Signal, das nach dem Speichern eines Modells ausgelöst wird
from django.dispatch import receiver  #Dekorator zur Registrierung von Signal-Empfängern
from .models import Profile #Importiert das Profile-Modell zur automatischen Profilerstellung


#Ermittelt das im Projekt verwendete User-Modell
User = get_user_model()


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    """
    Erstellt automatisch ein Profil für neu angelegte Benutzer
    """
    if created:
        Profile.objects.get_or_create(user=instance)
