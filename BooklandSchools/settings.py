import os
from pathlib import Path
import dj_database_url  # Requires: pip install dj-database-url

# =====================================================
# BASE DIRECTORY
# =====================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================================
# ENVIRONMENT VARIABLES & SECURITY
# =====================================================
# Get SECRET_KEY from environment
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-dev-key-fallback")

# Get DEBUG status from environment. Defaults to False for safety.
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Define ALL allowed host domains for security
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    # Specific production domains:
    "booklandbackend.onrender.com",  # <-- YOUR CONFIRMED RENDER DOMAIN
    ".onrender.com",  # Allows subdomains
]

# =====================================================
# APPLICATIONS
# =====================================================
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "corsheaders",  # For cross-origin requests from Vercel
    "rest_framework",

    # Local
    "booklandapp",
]

# =====================================================
# MIDDLEWARE
# =====================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # For static files (must be near top)
    "corsheaders.middleware.CorsMiddleware",      # For Vercel communication (must be very high)

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =====================================================
# URLS / WSGI
# =====================================================
ROOT_URLCONF = "BooklandSchools.urls"
WSGI_APPLICATION = "BooklandSchools.wsgi.application"

# =====================================================
# TEMPLATES (API only)
# =====================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# =====================================================
# DATABASE (Production-ready configuration)
# =====================================================

# Default to SQLite for local development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# If DATABASE_URL is set (e.g., by Render's PostgreSQL connection), use it.
DB_FROM_ENV = dj_database_url.config(conn_max_age=600)
if DB_FROM_ENV:
    DATABASES["default"].update(DB_FROM_ENV)


# =====================================================
# INTERNATIONALIZATION & PASSWORDS (Unchanged)
# =====================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =====================================================
# STATIC & MEDIA FILES (Whitenoise Setup)
# =====================================================
STATIC_URL = "/static/"
# Directory where static files will be collected for deployment
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# =====================================================
# CORS CONFIGURATION (Allow Vercel Frontend)
# =====================================================
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://bookland-frontend-lilac.vercel.app",  # <--- YOUR LIVE VERCEL URL
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "origin",
    "x-csrftoken",
    "x-requested-with",
]


# =====================================================
# CSRF TRUSTED ORIGINS (For secure POST requests)
# =====================================================
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "https://booklandbackend.onrender.com",         # <-- YOUR CONFIRMED RENDER DOMAIN
    "https://bookland-frontend-lilac.vercel.app",  # <--- YOUR LIVE VERCEL URL
]
