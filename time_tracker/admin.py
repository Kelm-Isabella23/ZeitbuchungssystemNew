from django.contrib import admin
from .models import Profile, Module, Report, RoleRequest


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "is_blocked")
    list_filter = ("role", "is_blocked")
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
    ordering = ("-created_at",)


@admin.register(RoleRequest)
class RoleRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "requested_role", "status", "created_at")
    list_filter = ("requested_role", "status")
    search_fields = ("user__username",)
    ordering = ("-created_at",)
