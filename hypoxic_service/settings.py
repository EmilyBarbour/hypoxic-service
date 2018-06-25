"""Settings for Hypoxic Service"""
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Secrets are overwritten on servers and should not be checked into repos.
SECRET_KEY = 'django_secret_key_placeholder'
VERSION = os.getenv('VERSION', '0.0.0')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hypoxic_admin',
    'hypoxic_otp',
    'hypoxic_service',
    'django_filters',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    'djoser',
    'rest_framework',
)

AUTH_USER_MODEL = 'hypoxic_admin.HypoxicUser'

DJOSER = {
    'ACTIVATION_URL': 'api/user/activate/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL': 'api/password/reset/confirm/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=15),
    'JWT_GET_USER_SECRET_KEY': 'hypoxic_admin.utils.jwt_get_secret_key',
    'JWT_PAYLOAD_HANDLER': 'hypoxic_otp.utils.jwt_otp_payload_handler',
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}
# 2FA issuer name
OTP_TOTP_ISSUER = 'Hypoxic'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hypoxic_service',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'dinopuppy',
        'PASSWORD': 'yppuponid',
        'CHARSET': 'utf8mb4',
        'COLLATION': 'utf8mb4_general_ci',
        'OPTIONS': {
            'sql_mode': 'STRICT_ALL_TABLES'
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
]

# Django session settings
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_NAME = "hypoxic"
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


STATIC_URL = '/static/'
STATIC_ROOT = '/var/hypoxic_service/static/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(threadName)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'hypoxic_service': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        # Uncomment to debug queries/performance
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        # },
    }
}

ROOT_URLCONF = 'hypoxic_service.urls'
WSGI_APPLICATION = 'hypoxic_service.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_PAGINATION_CLASS':
        'hypoxic_service.pagination.PageNumberPagination',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'ORDERING_PARAM': 'sort',
    'PAGE_SIZE': 20,
}
JSON_API_FORMAT_TYPES = 'dasherize'
JSON_API_PLURALIZE_TYPES = False
JSON_API_FORMAT_KEYS = 'underscore'

AWS_REGION = 'us-east-1'

# Email settings
SERVER_EMAIL = 'admin@notacoat.com'
DEFAULT_FROM_EMAIL = 'admin@notacoat.com'

USER_AGENT_STRING = 'hypoxic-service/{}'.format(VERSION)
