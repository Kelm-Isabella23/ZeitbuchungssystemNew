# Initiale Migration der time_tracker-App
# Erstellt die Datenbanktabellen basierend auf den Modellen

# Enthält Löschstrategien (CASCADE, PROTECT, etc.) für ForeignKeys
import django.db.models.deletion

# Zugriff auf die Django-Settings (z. B. AUTH_USER_MODEL)
from django.conf import settings

# Django-Migrations-Framework:
# migrations: Steuerung von Migrationen
# models: Feldtypen für Datenbanktabellen
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Initiale Migration der time_tracker-App.

    Erstellt alle Tabellen, die für die App benötigt werden.
    """

    # Kennzeichnet diese Migration als erste Migration der App
    initial = True

    # Abhängigkeit vom User-Modell (auch bei Custom Usern korrekt)
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    # Datenbankoperationen, die bei der Migration ausgeführt werden
    operations = [
        # =========================
        # Modul-Tabelle
        # =========================
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('name', models.CharField(
                    max_length=100,
                    unique=True
                )),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),

        # =========================
        # Profil-Tabelle
        # =========================
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('role', models.CharField(
                    choices=[('USER', 'User'), ('VIP', 'VIP'), ('ADMIN', 'Admin')],
                    default='USER',
                    max_length=10
                )),
                ('is_blocked', models.BooleanField(default=False)),

                # Verknüpfung zum Django-User (1:1)
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),

        # =========================
        # Report-Tabelle (Zeitbuchungen)
        # =========================
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('date', models.DateField()),
                ('minutes', models.PositiveIntegerField()),
                ('text', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),

                # Modul darf nicht gelöscht werden, solange Reports existieren
                ('module', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    to='time_tracker.module'
                )),

                # Verknüpfung zum Benutzer
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),

        # =========================
        # Rollen-Anträge
        # =========================
        migrations.CreateModel(
            name='RoleRequest',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('requested_role', models.CharField(
                    choices=[('VIP', 'VIP'), ('ADMIN', 'Admin')],
                    max_length=10
                )),
                ('status', models.CharField(
                    choices=[
                        ('PENDING', 'Pending'),
                        ('APPROVED', 'Approved'),
                        ('REJECTED', 'Rejected')
                    ],
                    default='PENDING',
                    max_length=10
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),

                # Antragsteller
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),
    ]
