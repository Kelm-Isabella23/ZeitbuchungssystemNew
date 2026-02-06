from django.contrib import admin # Stellt die Django-Admin-Funktionalitäten bereit (Ermöglicht das Registrieren und Anpassen von Modellen im Admin-Backend)
from .models import Profile, Module, Report, RoleRequest # Importiert die Datenmodelle der time_tracker-App, die im Admin-Bereich verwaltet werden sollen


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    # Spaltenübersicht in der Listenansicht
    list_display = ("user", "role", "is_blocked")

    # Filteroptionen in der rechten Seitenleiste
    list_filter = ("role", "is_blocked")

    # Suchfelder (inkl. Felder aus verknüpften Modellen)
    search_fields = ("user__username", "user__email")


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):

    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):

    list_display = ("user", "date", "minutes", "module", "created_at")
    list_filter = ("module", "date")
    search_fields = ("user__username", "text")

    # Sortiert Einträge standardmäßig nach Erstellungsdatum (neueste zuerst)
    ordering = ("-created_at",)


@admin.register(RoleRequest)
class RoleRequestAdmin(admin.ModelAdmin):
    """
    Admin-Konfiguration für Rollenanfragen von Benutzern.
    (Dient zur Prüfung und Bearbeitung von
    Berechtigungsanfragen im System)
    """

    list_display = ("user", "requested_role", "status", "created_at")
    list_filter = ("requested_role", "status")
    search_fields = ("user__username",)
    ordering = ("-created_at",)
