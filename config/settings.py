import logging.config
import os

import environ

ROOT_DIR = environ.Path(__file__) - 2
APPS_DIR = ROOT_DIR.path("chemreg")

env = environ.Env(
    CACHE_URL=(str, "locmemcache://"),
    COMPOUND_PREFIX=(str, ""),
    DATABASE_URL=(str, "sqlite:///.sqlite3"),
    DEBUG=(bool, True),
    RESOLUTION_URL=(str, ""),
    SESSION_COOKIE_AGE=(int, 900),
    SECRET_KEY=(str, "secret"),
    URL_CONF=(str, "api"),
    WHITELIST_CORS=(str, ""),
    WHITELIST_HOST=(str, ""),
    WHITELIST_LOCAL=(bool, True),
    WEB_CONCURRENCY=(int, 1),
)
if os.path.exists(ROOT_DIR(".env")):
    env.read_env(ROOT_DIR(".env"))

#################
# Core Settings #
#    django     #
#################
# https://docs.djangoproject.com/en/3.0/ref/settings/#core-settings

ALLOWED_HOSTS = []
if env.bool("WHITELIST_LOCAL"):
    ALLOWED_HOSTS += [
        "0.0.0.0",
        "127.0.0.1",
        "localhost",
        "testserver",
    ]
if env("WHITELIST_HOST"):
    ALLOWED_HOSTS += [env("WHITELIST_HOST")]
CACHES = {"default": env.cache_url("CACHE_URL", env("CACHE_URL"))}
COMPOUND = {"PREFIX": env("COMPOUND_PREFIX", default="DTX")}
DATABASES = {"default": env.db_url("DATABASE_URL", env("DATABASE_URL"))}
DEBUG = env("DEBUG")
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    # Third party apps
    "computed_property",
    "django_prometheus",
    "html_sanitizer",
    "polymorphic",
    "rest_framework",
    "partialsmiles",
    # Local apps
    "chemreg.auth.apps.AuthConfig",
    "chemreg.common.apps.CommonConfig",
    "chemreg.compound.apps.CompoundConfig",
    "chemreg.lists.apps.ListsConfig",
    "chemreg.openapi.apps.OpenAPIConfig",
    "chemreg.resolution.apps.ResolutionConfig",
    "chemreg.substance.apps.SubstanceConfig",
    "chemreg.users.apps.UsersConfig",
    "chemreg.utils.apps.UtilsConfig",
]
MEDIA_ROOT = APPS_DIR("media")
MEDIA_URL = "/media/"
MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "crum.CurrentRequestUserMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]
ROOT_URLCONF = "config.urls." + env("URL_CONF")
SECRET_KEY = env("SECRET_KEY")
TEMPLATES = [
    {
        "APP_DIRS": True,
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]
TIME_ZONE = "UTC"
USE_I18N = False
WSGI_APPLICATION = "config.wsgi.application"

###########################
#    Resolver Settings    #
###########################
RESOLUTION_URL = env("RESOLUTION_URL")


#######################
#    Auth Settings    #
# django.contrib.auth #
#######################
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "login/"
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

###########################
#    Session Settings     #
# django.contrib.sessions #
###########################
# https://docs.djangoproject.com/en/3.0/ref/settings/#sessions

SESSION_COOKIE_AGE = env("SESSION_COOKIE_AGE")
SESSION_COOKIE_SAMESITE = "Strict"
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_SAVE_EVERY_REQUEST = True

##############################
#    Static Files Settings   #
# django.contrib.staticfiles #
##############################
# https://docs.djangoproject.com/en/3.0/ref/settings/#static-files

STATIC_ROOT = ROOT_DIR("collected_static")
STATIC_URL = "/static/"

#######################
#    CORS Settings    #
# django-cors-headers #
#######################
# https://github.com/adamchainz/django-cors-headers#configuration

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_REGEX_WHITELIST = []
if env("WHITELIST_LOCAL"):
    CORS_ORIGIN_REGEX_WHITELIST += [
        r"^http://0\.0\.0\.0:\d+$",
        r"^https://0\.0\.0\.0:\d+$",
        r"^http://127\.0\.0\.1:\d+$",
        r"^https://127\.0\.0\.1:\d+$",
        r"^http://localhost:\d+$",
        r"^https://localhost:\d+$",
    ]
CORS_ORIGIN_WHITELIST = []
if env("WHITELIST_CORS"):
    CORS_ORIGIN_WHITELIST += ["https://" + env("WHITELIST_CORS")]

#######################
#  Gunicorn Settings  #
#      gunicorn       #
#######################
# https://docs.gunicorn.org/en/latest/settings.html

WEB_CONCURRENCY = env("WEB_CONCURRENCY")

####################################
#  Django REST Framework Settings  #
#          rest_framework          #
####################################
# https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "chemreg.auth.authentication.CsrfExemptSessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework_json_api.filters.QueryParameterValidationFilter",
        "rest_framework_json_api.filters.OrderingFilter",
        "rest_framework_json_api.django_filters.DjangoFilterBackend",
        # "rest_framework.filters.SearchFilter",
    ],
    "DEFAULT_METADATA_CLASS": "rest_framework_json_api.metadata.JSONAPIMetadata",
    "DEFAULT_PAGINATION_CLASS": "chemreg.jsonapi.pagination.JsonApiPageNumberPagination",
    "DEFAULT_PARSER_CLASSES": ["chemreg.jsonapi.parsers.JSONParser"],
    "DEFAULT_PERMISSION_CLASSES": [
        # "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_RENDERER_CLASSES": ["chemreg.jsonapi.renderers.JSONRenderer"],
    "EXCEPTION_HANDLER": "rest_framework_json_api.exceptions.exception_handler",
    "PAGE_SIZE": 100,
    # "SEARCH_PARAM": "filter[search]",
    "TEST_REQUEST_DEFAULT_FORMAT": "vnd.api+json",
    "TEST_REQUEST_RENDERER_CLASSES": ["chemreg.jsonapi.renderers.JSONRenderer"],
}

#############################################
#  Django REST Framework JSON API Settings  #
#          rest_framework_json_api          #
#############################################
# https://django-rest-framework-json-api.readthedocs.io/en/stable/usage.html#configuration

JSON_API_FORMAT_FIELD_NAMES = "camelize"
JSON_API_FORMAT_TYPES = "camelize"

#########################
#  WhiteNoise Settings  #
#      whitenoise       #
#########################
# http://whitenoise.evans.io/en/stable/django.html

WHITENOISE_AUTOREFRESH = DEBUG
WHITENOISE_USE_FINDERS = DEBUG


#############################################
#          Logging Configuration            #
#                 logging                   #
#############################################
# https://docs.python.org/3/library/logging.html
# https://docs.gunicorn.org/en/stable/settings.html#access-log-format

LOGGING_CONFIG = None

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "%(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "[%d/%b/%Y %H:%M:%S]",
            "class": "logging.Formatter",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "console"},
    },
    "loggers": {
        "django": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

logging.config.dictConfig(LOGGING)
