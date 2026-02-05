# Zugriff auf die Django-Settings (z. B. AUTH_USER_MODEL)
# Ermöglicht die Verwendung des konfigurierten User-Modells
from django.conf import settings

# Stellt die Django-Model-Basisklassen und Feldtypen bereit
from django.db import models


class Profile(models.Model):
    """
    Erweitert den Django-Benutzer um zusätzliche Informationen.

    Speichert Rollen und Sperrstatus eines Benutzers
    für die Zugriffskontrolle innerhalb der Anwendung.
    """

    # Interne Rollendefinitionen
    ROLE_USER = "USER"
    ROLE_VIP = "VIP"
    ROLE_ADMIN = "ADMIN"

    # Auswahlmöglichkeiten für Rollenfelder
    ROLE_CHOICES = [
        (ROLE_USER, "User"),
        (ROLE_VIP, "VIP"),
        (ROLE_ADMIN, "Admin"),
    ]

    # Eins-zu-eins-Verknüpfung mit dem Django-Benutzer
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Rolle des Benutzers (Standard: normaler User)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_USER
    )

    # Kennzeichnet gesperrte Benutzer
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        # Textdarstellung für Admin-Backend und Debugging
        return f"{self.user.username} ({self.role})"


class Module(models.Model):
    """
    Repräsentiert ein Arbeits- oder Projektmodul,
    dem Zeitbuchungen zugeordnet werden können.
    """

    # Name des Moduls (muss eindeutig sein)
    name = models.CharField(max_length=100, unique=True)

    # Steuert, ob das Modul für neue Buchungen auswählbar ist
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Report(models.Model):
    """
    Speichert einzelne Zeitbuchungen eines Benutzers.

    Jede Buchung besteht aus Datum, Dauer,
    zugehörigem Modul und einer Beschreibung.
    """

    # Verknüpfung zur buchenden Person
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Datum der Arbeitsleistung
    date = models.DateField()

    # Dauer der Arbeit in Minuten
    minutes = models.PositiveIntegerField()

    # Zugeordnetes Modul (Löschen von Modulen wird verhindert)
    module = models.ForeignKey(
        Module,
        on_delete=models.PROTECT
    )

    # Kurzbeschreibung der Tätigkeit
    text = models.CharField(max_length=300)

    # Zeitstempel der Erstellung
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.minutes} min"


class RoleRequest(models.Model):
    """
    Modell für Anfragen zur Rollenänderung.

    Benutzer können hierüber erweiterte Rechte
    (z. B. VIP oder Admin) beantragen.
    """

    # Statusdefinitionen
    STATUS_PENDING = "PENDING"
    STATUS_APPROVED = "APPROVED"
    STATUS_REJECTED = "REJECTED"

    # Auswahlmöglichkeiten für den Status
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    # Mögliche Rollen, die beantragt werden können
    REQUEST_VIP = "VIP"
    REQUEST_ADMIN = "ADMIN"

    REQUEST_CHOICES = [
        (REQUEST_VIP, "VIP"),
        (REQUEST_ADMIN, "Admin"),
    ]

    # Antragstellender Benutzer
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Gewünschte Rolle
    requested_role = models.CharField(
        max_length=10,
        choices=REQUEST_CHOICES
    )

    # Aktueller Bearbeitungsstatus der Anfrage
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    # Zeitpunkt der Antragstellung
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.requested_role} ({self.status})"
