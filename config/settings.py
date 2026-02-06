"""
Zentrale Konfigurationsdatei des Django-Projekts
(Enthält alle grundlegenden Einstellungen wie Apps, Datenbank,
Sicherheit, Templates und statische Dateien)
"""

# Stellt die Path-Klasse bereit, um Dateipfade betriebssystemunabhängig zu verwalten
from pathlib import Path


# Basisverzeichnis des Projekts (wird für Pfadangaben im Projekt genutzt)
BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# Sicherheits- & Debug-Einstellungen
# =========================

# Geheimer Schlüssel für kryptografische Operationen (nur für Entwicklung!)
SECRET_KEY = 'django-insecure-s@^yx)!-35*$hujxzj-7fk2u=nd@%c0j4ndl3pg7j!48#n+dhu'

# Aktiviert Debug-Ausgaben (Fehlermeldungen, Tracebacks)
DEBUG = True

# Erlaubte Hosts, von denen auf die Anwendung zugegriffen werden darf
# (inkl. IPv4, IPv6, localhost und Servername)
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "::1",
    "servernew",
    "2001:7c0:2320:2f8:816:3eff:fe16:80d8",
    "2001:7c0:2320:2:f816:3eff:fe16:80d8",
    "[2001:7c0:2320:2:f816:3eff:fe16:80d8]",
]


# =========================
# Applikationsdefinition
# =========================

# Liste aller aktivierten Django-Apps
INSTALLED_APPS = [
    # Standard-Django-Komponenten
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Eigene Fachanwendung zur Zeitbuchung
    'time_tracker',
]


# Middleware zur Verarbeitung von Requests und Responses
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Verweist auf die zentrale URL-Konfiguration des Projekts
ROOT_URLCONF = 'config.urls'


# =========================
# Template-Konfiguration
# =========================

TEMPLATES = [
    {
        # Verwendetes Template-Backend
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Globales Template-Verzeichnis (projektweit)
        'DIRS': [BASE_DIR / "templates"],

        # Zusätzlich Templates aus den App-Verzeichnissen laden
        'APP_DIRS': True,

        # Kontextdaten, die automatisch in Templates verfügbar sind
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# WSGI-Einstiegspunkt für Deployment (z. B. Gunicorn)
WSGI_APPLICATION = 'config.wsgi.application'


# =========================
# Datenbank-Konfiguration
# =========================

# Verwendet SQLite als einfache Entwicklungsdatenbank
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =========================
# Passwort-Sicherheitsregeln
# =========================

# Validierungsregeln für Benutzerpasswörter
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =========================
# Internationalisierung
# =========================

# Standardsprache der Anwendung
LANGUAGE_CODE = 'en-us'

# Zeitzone des Systems
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True


# =========================
# Statische Dateien (CSS, JS, Bilder)
# =========================

# URL-Pfad für statische Dateien
STATIC_URL = 'static/'

# Zusätzliches Verzeichnis für statische Dateien im Projekt
STATICFILES_DIRS = [BASE_DIR / "static"]


# =========================
# Standard-Primärschlüssel
# =========================

# Standardtyp für automatisch erzeugte Primärschlüssel
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'