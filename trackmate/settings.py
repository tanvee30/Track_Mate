# # # # import os
# # # # from pathlib import Path
# # # # from datetime import timedelta
# # # # from django.core.management.utils import get_random_secret_key
# # # #
# # # # BASE_DIR = Path(__file__).resolve().parent.parent
# # # #
# # # # SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", get_random_secret_key())
# # # # DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"
# # # # ALLOWED_HOSTS = ["*"]
# # # #
# # # # INSTALLED_APPS = [
# # # #     "django.contrib.admin",
# # # #     "django.contrib.auth",
# # # #     "django.contrib.contenttypes",
# # # #     "django.contrib.sessions",
# # # #     "django.contrib.messages",
# # # #     "django.contrib.staticfiles",
# # # #
# # # #     "rest_framework",
# # # #     "rest_framework_simplejwt.token_blacklist",
# # # #
# # # #     "auth_app",
# # # #     "profile_app",
# # # # ]
# # # #
# # # # MEDIA_URL = '/media/'
# # # # MEDIA_ROOT = BASE_DIR / 'media'
# # # #
# # # # AUTH_USER_MODEL = "auth_app.User"
# # # #
# # # # MIDDLEWARE = [
# # # #     "django.middleware.security.SecurityMiddleware",
# # # #     "django.contrib.sessions.middleware.SessionMiddleware",
# # # #     "django.middleware.common.CommonMiddleware",
# # # #     "django.middleware.csrf.CsrfViewMiddleware",
# # # #     "django.contrib.auth.middleware.AuthenticationMiddleware",
# # # #     "django.contrib.messages.middleware.MessageMiddleware",
# # # #     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# # # # ]
# # # #
# # # # ROOT_URLCONF = "trackmate.urls"
# # # #
# # # # TEMPLATES = [
# # # #     {
# # # #         "BACKEND": "django.template.backends.django.DjangoTemplates",
# # # #         "DIRS": [],
# # # #         "APP_DIRS": True,
# # # #         "OPTIONS": {
# # # #             "context_processors": [
# # # #                 "django.template.context_processors.debug",
# # # #                 "django.template.context_processors.request",
# # # #                 "django.contrib.auth.context_processors.auth",
# # # #                 "django.contrib.messages.context_processors.messages",
# # # #             ],
# # # #         },
# # # #     },
# # # # ]
# # # #
# # # # WSGI_APPLICATION = "trackmate.wsgi.application"
# # # #
# # # # DATABASES = {
# # # #     "default": {
# # # #         "ENGINE": "django.db.backends.sqlite3",
# # # #         "NAME": BASE_DIR / "db.sqlite3",
# # # #     }
# # # # }
# # # #
# # # # AUTH_PASSWORD_VALIDATORS = [
# # # #     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
# # # #     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
# # # #     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
# # # #     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# # # # ]
# # # #
# # # # LANGUAGE_CODE = "en-us"
# # # # TIME_ZONE = "UTC"
# # # # USE_I18N = True
# # # # USE_TZ = True
# # # #
# # # # STATIC_URL = "/static/"
# # # # STATIC_ROOT = BASE_DIR / "staticfiles"
# # # #
# # # # REST_FRAMEWORK = {
# # # #     "DEFAULT_AUTHENTICATION_CLASSES": (
# # # #         "rest_framework_simplejwt.authentication.JWTAuthentication",
# # # #     )
# # # # }
# # # #
# # # # SIMPLE_JWT = {
# # # #     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
# # # #     "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
# # # # }
# # # #
# # # # EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# # # # EMAIL_HOST = "smtp.gmail.com"
# # # # EMAIL_PORT = 587
# # # # EMAIL_USE_TLS = True
# # # #
# # # # EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "teamyuktek@gmail.com")
# # # # EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "kavk rydz yebl cibq")
# # # #
# # # # DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# # # #
# # # # DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# # #
# # # import os
# # # from dotenv import load_dotenv
# # # from pathlib import Path
# # # from datetime import timedelta
# # # from django.core.management.utils import get_random_secret_key
# # # import dj_database_url
# # #
# # #
# # #
# # # load_dotenv()
# # #
# # #
# # # BASE_DIR = Path(__file__).resolve().parent.parent
# # #
# # # SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", get_random_secret_key())
# # # DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"  # Changed default to False for production
# # # ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")
# # #
# # # INSTALLED_APPS = [
# # #     "django.contrib.admin",
# # #     "django.contrib.auth",
# # #     "django.contrib.contenttypes",
# # #     "django.contrib.sessions",
# # #     "django.contrib.messages",
# # #     "django.contrib.staticfiles",
# # #     "corsheaders",
# # #
# # #
# # #     "rest_framework",
# # #     "rest_framework_simplejwt.token_blacklist",
# # #
# # #     "auth_app",
# # #     "profile_app",
# # # ]
# # #
# # # MEDIA_URL = '/media/'
# # # MEDIA_ROOT = BASE_DIR / 'media'
# # #
# # # AUTH_USER_MODEL = "auth_app.User"
# # #
# # # MIDDLEWARE = [
# # #     "django.middleware.security.SecurityMiddleware",
# # #     "django.contrib.sessions.middleware.SessionMiddleware",
# # #     "django.middleware.common.CommonMiddleware",
# # #     "django.middleware.csrf.CsrfViewMiddleware",
# # #     "django.contrib.auth.middleware.AuthenticationMiddleware",
# # #     "django.contrib.messages.middleware.MessageMiddleware",
# # #     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# # #     "corsheaders.middleware.CorsMiddleware",
# # #     "whitenoise.middleware.WhiteNoiseMiddleware",
# # #
# # # ]
# # #
# # # CORS_ALLOW_ALL_ORIGINS = True
# # #
# # #
# # # ROOT_URLCONF = "trackmate.urls"
# # #
# # # TEMPLATES = [
# # #     {
# # #         "BACKEND": "django.template.backends.django.DjangoTemplates",
# # #         "DIRS": [],
# # #         "APP_DIRS": True,
# # #         "OPTIONS": {
# # #             "context_processors": [
# # #                 "django.template.context_processors.debug",
# # #                 "django.template.context_processors.request",
# # #                 "django.contrib.auth.context_processors.auth",
# # #                 "django.contrib.messages.context_processors.messages",
# # #             ],
# # #         },
# # #     },
# # # ]
# # #
# # # WSGI_APPLICATION = "trackmate.wsgi.application"
# # # <<<<<<< HEAD
# # # ASGI_APPLICATION = "trackmate.asgi.application"
# # #
# # # # -------------------------
# # # # DATABASE (SQLite)
# # # # -------------------------
# # #
# # # if os.environ.get("DATABASE_URL"):
# # #     # Use PostgreSQL on Railway
# # #     DATABASES = {
# # #         "default": dj_database_url.config(
# # #             conn_max_age=600,
# # #             ssl_require=False,
# # #         )
# # # =======
# # #
# # # DATABASES = {
# # #     "default": {
# # #         "ENGINE": "django.db.backends.sqlite3",
# # #         "NAME": BASE_DIR / "db.sqlite3",
# # # >>>>>>> profile_api
# # #     }
# # # else:
# # #     # Use SQLite locally
# # #     DATABASES = {
# # #         "default": {
# # #             "ENGINE": "django.db.backends.sqlite3",
# # #             "NAME": BASE_DIR / "db.sqlite3",
# # #         }
# # #     }
# # #
# # #
# # # AUTH_PASSWORD_VALIDATORS = [
# # #     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
# # #     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
# # #     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
# # #     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# # # ]
# # #
# # # LANGUAGE_CODE = "en-us"
# # # TIME_ZONE = "UTC"
# # # USE_I18N = True
# # # USE_TZ = True
# # #
# # # <<<<<<< HEAD
# # # # -------------------------
# # # # STATIC FILES
# # # # -------------------------
# # # =======
# # # >>>>>>> profile_api
# # # STATIC_URL = "/static/"
# # # STATIC_ROOT = BASE_DIR / "staticfiles"
# # #
# # # REST_FRAMEWORK = {
# # #     "DEFAULT_AUTHENTICATION_CLASSES": (
# # #         "rest_framework_simplejwt.authentication.JWTAuthentication",
# # #     )
# # # }
# # #
# # # SIMPLE_JWT = {
# # #     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
# # #     "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
# # # }
# # #
# # # EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# # # EMAIL_HOST = "smtp.gmail.com"
# # # EMAIL_PORT = 587
# # # EMAIL_USE_TLS = True
# # # EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "teamyuktek@gmail.com")
# # # EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "kavk rydz yebl cibq")
# # #
# # #
# # #
# # # DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# # #
# # # DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# # import os
# # from dotenv import load_dotenv
# # from pathlib import Path
# # from datetime import timedelta
# # from django.core.management.utils import get_random_secret_key
# # import dj_database_url
# #
# # load_dotenv()
# #
# # BASE_DIR = Path(__file__).resolve().parent.parent
# #
# # SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", get_random_secret_key())
# # # DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"
# # DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"
# #
# # ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")
# #
# # INSTALLED_APPS = [
# #     "django.contrib.admin",
# #     "django.contrib.auth",
# #     "django.contrib.contenttypes",
# #     "django.contrib.sessions",
# #     "django.contrib.messages",
# #     "django.contrib.staticfiles",
# #     "corsheaders",
# #
# #     "rest_framework",
# #     "rest_framework_simplejwt.token_blacklist",
# #
# #     "auth_app",
# #     "profile_app",
# # ]
# #
# # MEDIA_URL = '/media/'
# # MEDIA_ROOT = BASE_DIR / 'media'
# #
# # AUTH_USER_MODEL = "auth_app.User"
# #
# # MIDDLEWARE = [
# #     "django.middleware.security.SecurityMiddleware",
# #     "django.contrib.sessions.middleware.SessionMiddleware",
# #     "django.middleware.common.CommonMiddleware",
# #     "django.middleware.csrf.CsrfViewMiddleware",
# #     "django.contrib.auth.middleware.AuthenticationMiddleware",
# #     "django.contrib.messages.middleware.MessageMiddleware",
# #     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# #     "corsheaders.middleware.CorsMiddleware",
# #     "whitenoise.middleware.WhiteNoiseMiddleware",
# # ]
# #
# # CORS_ALLOW_ALL_ORIGINS = True
# #
# # ROOT_URLCONF = "trackmate.urls"
# #
# # TEMPLATES = [
# #     {
# #         "BACKEND": "django.template.backends.django.DjangoTemplates",
# #         "DIRS": [],
# #         "APP_DIRS": True,
# #         "OPTIONS": {
# #             "context_processors": [
# #                 "django.template.context_processors.debug",
# #                 "django.template.context_processors.request",
# #                 "django.contrib.auth.context_processors.auth",
# #                 "django.contrib.messages.context_processors.messages",
# #             ],
# #         },
# #     },
# # ]
# #
# # WSGI_APPLICATION = "trackmate.wsgi.application"
# # ASGI_APPLICATION = "trackmate.asgi.application"
# #
# # # ----------------------------------------------------
# # # DATABASE CONFIGURATION (Railway → PostgreSQL / Local → SQLite)
# # # ----------------------------------------------------
# # if os.environ.get("DATABASE_URL"):
# #     DATABASES = {
# #         "default": dj_database_url.config(
# #             conn_max_age=600,
# #             ssl_require=False,
# #         )
# #     }
# # else:
# #     DATABASES = {
# #         "default": {
# #             "ENGINE": "django.db.backends.sqlite3",
# #             "NAME": BASE_DIR / "db.sqlite3",
# #         }
# #     }
# #
# # AUTH_PASSWORD_VALIDATORS = [
# #     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
# #     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
# #     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
# #     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# # ]
# #
# # LANGUAGE_CODE = "en-us"
# # TIME_ZONE = "UTC"
# # USE_I18N = True
# # USE_TZ = True
# #
# # STATIC_URL = "/static/"
# # STATIC_ROOT = BASE_DIR / "staticfiles"
# #
# # STATICFILES_DIRS = [
# #     BASE_DIR / "static",
# # ]
# #
# # REST_FRAMEWORK = {
# #     "DEFAULT_AUTHENTICATION_CLASSES": (
# #         "rest_framework_simplejwt.authentication.JWTAuthentication",
# #     )
# # }
# #
# # SIMPLE_JWT = {
# #     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
# #     "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
# # }
# #
# # EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# # EMAIL_HOST = "smtp.gmail.com"
# # EMAIL_PORT = 587
# # EMAIL_USE_TLS = True
# # EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "teamyuktek@gmail.com")
# # EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "kavk rydz yebl cibq")
# #
# # DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# #
# # DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
#
# import os
# from pathlib import Path
# from datetime import timedelta
# from django.core.management.utils import get_random_secret_key
# from dotenv import load_dotenv
# import dj_database_url
#
# load_dotenv()
#
# # ---------------------------------------------------------
# # BASE DIRECTORY
# # ---------------------------------------------------------
# BASE_DIR = Path(__file__).resolve().parent.parent
#
#
# # ---------------------------------------------------------
# # SECURITY SETTINGS
# # ---------------------------------------------------------
# SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", get_random_secret_key())
# DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"
# ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")
#
#
# # ---------------------------------------------------------
# # INSTALLED APPS
# # ---------------------------------------------------------
# INSTALLED_APPS = [
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#
#     "corsheaders",
#
#     "rest_framework",
#     "rest_framework_simplejwt",
#     "rest_framework_simplejwt.token_blacklist",
#
#     "auth_app",
#     "profile_app",
# ]
#
#
# # ---------------------------------------------------------
# # CUSTOM USER MODEL
# # ---------------------------------------------------------
# AUTH_USER_MODEL = "auth_app.User"
#
#
# # ---------------------------------------------------------
# # MIDDLEWARE
# # ---------------------------------------------------------
# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#
#     # Whitenoise MUST be just below SecurityMiddleware
#     "whitenoise.middleware.WhiteNoiseMiddleware",
#
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "corsheaders.middleware.CorsMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]
#
#
# # ---------------------------------------------------------
# # CORS
# # ---------------------------------------------------------
# CORS_ALLOW_ALL_ORIGINS = True
#
#
# # ---------------------------------------------------------
# # URL CONFIGURATION
# # ---------------------------------------------------------
# ROOT_URLCONF = "trackmate.urls"
#
#
# # ---------------------------------------------------------
# # TEMPLATES
# # ---------------------------------------------------------
# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.debug",
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]
#
#
# # ---------------------------------------------------------
# # WSGI + ASGI
# # ---------------------------------------------------------
# WSGI_APPLICATION = "trackmate.wsgi.application"
# ASGI_APPLICATION = "trackmate.asgi.application"
#
#
# # ---------------------------------------------------------
# # DATABASE SETTINGS
# # ---------------------------------------------------------
# if os.environ.get("DATABASE_URL"):
#     DATABASES = {
#         "default": dj_database_url.config(
#             conn_max_age=600,
#             ssl_require=False
#         )
#     }
# else:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": BASE_DIR / "db.sqlite3",
#         }
#     }
#
#
# # ---------------------------------------------------------
# # PASSWORD VALIDATION
# # ---------------------------------------------------------
# AUTH_PASSWORD_VALIDATORS = [
#     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# ]
#
#
# # ---------------------------------------------------------
# # INTERNATIONALIZATION
# # ---------------------------------------------------------
# LANGUAGE_CODE = "en-us"
# TIME_ZONE = "UTC"
# USE_I18N = True
# USE_TZ = True
#
#
# # ---------------------------------------------------------
# # STATIC + MEDIA FILES
# # ---------------------------------------------------------
# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"
#
# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"
#
# # Whitenoise: Serve static files
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
#
#
# # ---------------------------------------------------------
# # REST FRAMEWORK + JWT
# # ---------------------------------------------------------
# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "rest_framework_simplejwt.authentication.JWTAuthentication",
#     ),
# }
#
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
#     "BLACKLIST_AFTER_ROTATION": True,
#     "AUTH_HEADER_TYPES": ("Bearer",),
# }
#
#
# # ---------------------------------------------------------
# # EMAIL SETTINGS
# # ---------------------------------------------------------
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "teamyuktek@gmail.com")
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "kavk rydz yebl cibq")
#
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
#
#
# # ---------------------------------------------------------
# # AUTO FIELD
# # ---------------------------------------------------------
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

import os
from pathlib import Path
from datetime import timedelta
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv
load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", get_random_secret_key())
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",

    "auth_app",
    "trips",
    "profile_app",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = "auth_app.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "trackmate.urls"

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

WSGI_APPLICATION = "trackmate.wsgi.application"
ASGI_APPLICATION = "TrackMate.asgi.application"

# -------------------------
# DATABASE (SQLite)
# -------------------------
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": 'trackmate_db',
        "USER": 'trackmate_user',
        "PASSWORD": 'ATM263014@atm',
        "HOST": 'localhost,
        "PORT": '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -------------------------
# STATIC FILES (FIXED)
# -------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "teamyuktek@gmail.com")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "kavk rydz yebl cibq")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

GOOGLE_MAPS_API_KEY = "AIzaSyB5K4jC0T_r3R43lfwP55vxt3lXNf-E-lk"
GOOGLE_GEOCODING_API_KEY = "AIzaSyCIuctlZtylqWYpH8NZ_y8hdqQ0P5JhlHM"
GOOGLE_DIRECTIONS_API_KEY = "AIzaSyDFTdr7PpBNjhE6yufD7mRfLu5yEoIV9SI"
