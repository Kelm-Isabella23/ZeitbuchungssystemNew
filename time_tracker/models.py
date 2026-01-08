from django.conf import settings
from django.db import models


class Profile(models.Model):
    ROLE_USER = "USER"
    ROLE_VIP = "VIP"
    ROLE_ADMIN = "ADMIN"

    ROLE_CHOICES = [
        (ROLE_USER, "User"),
        (ROLE_VIP, "VIP"),
        (ROLE_ADMIN, "Admin"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Module(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    minutes = models.PositiveIntegerField()
    module = models.ForeignKey(Module, on_delete=models.PROTECT)
    text = models.CharField(max_length=300)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.minutes} min"


class RoleRequest(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_APPROVED = "APPROVED"
    STATUS_REJECTED = "REJECTED"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    REQUEST_VIP = "VIP"
    REQUEST_ADMIN = "ADMIN"
    REQUEST_CHOICES = [
        (REQUEST_VIP, "VIP"),
        (REQUEST_ADMIN, "Admin"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    requested_role = models.CharField(max_length=10, choices=REQUEST_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.requested_role} ({self.status})"
