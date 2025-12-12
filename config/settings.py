import os
from datetime import timedelta
from logging import debug
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment variables.")

SECRET_KEY_API = os.getenv("SECRET_KEY_API", "fallback-secret-key")
if not SECRET_KEY_API:
    raise ValueError("SECRET_KEY_API is not set in the environment variables.")


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-jwt-secret-key")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY is not set in the environment variables.")


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent
#log
# from .logging import LOGGING
# Debug mode
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PACKAGES_APPS = [
    'rest_framework',
    'django_filters',
    'import_export',
    'drf_standardized_errors',
    'rest_framework_simplejwt',
    'django_celery_beat',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "auditlog",
    'channels',
    'channels_redis',
    'storages',
    'debug_toolbar'
]
PROJECT_APPS = [
    'config',
    'core',
    'post'
]
INSTALLED_APPS = PACKAGES_APPS + PROJECT_APPS + DJANGO_APPS



MIDDLEWARE = [
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'config.logging.RequestLoggingMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'live_logs.middleware.RequestContextMiddleware',
    'auditlog.middleware.AuditlogMiddleware'
]


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# Custom user model
# AUTH_USER_MODEL = 'core.CustomUser'
# AUTH_GROUP_MODEL = 'authentication.Group'
# AUTH_PERMISSION_MODEL = 'authentication.Permission'

WSGI_APPLICATION = 'config.wsgi.application'

ASGI_APPLICATION = "config.asgi.application"

# Database configuration
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': os.getenv("POSTGRES_DB"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        'HOST': os.getenv("POSTGRES_HOST"),
        'PORT': os.getenv("POSTGRES_PORT"),
        'CONN_MAX_AGE': 60,
        'DISABLE_SERVER_SIDE_CURSORS': True,
    }
}
#click house
# CLICKHOUSE_HOST = os.getenv('CLICKHOUSE_HOST')
# CLICKHOUSE_PORT = int(os.getenv('CLICKHOUSE_PORT'))
# CLICKHOUSE_USER = os.getenv('CLICKHOUSE_USER')
# CLICKHOUSE_PASS = os.getenv('CLICKHOUSE_PASS')
# CLICKHOUSE_DB   = os.getenv('CLICKHOUSE_DB')

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    # {'NAME': 'django.contrib.authentication.password_validation.UserAttributeSimilarityValidator'},
    # {'NAME': 'django.contrib.authentication.password_validation.MinimumLengthValidator'},
    # {'NAME': 'django.contrib.authentication.password_validation.CommonPasswordValidator'},
    # {'NAME': 'django.contrib.authentication.password_validation.NumericPasswordValidator'},
]

# JWT Configuration
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=int(os.getenv("ACCESS_TOKEN_LIFETIME", 1))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("REFRESH_TOKEN_LIFETIME", 7))),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": os.getenv("JWT_SIGNING_KEY"),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}
# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny'],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    # 'DEFAULT_RENDERER_CLASSES': [
    #     'common.exceptions.CustomJSONRenderer',
    #     'rest_framework.renderers.BrowsableAPIRenderer',
    # ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # anonouse user
        'user': '1000/hour',  # ath user
    },
    "EXCEPTION_HANDLER": "common.exceptions.exception_handler",
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'IMP API Documentation',
    'SERVE_INCLUDE_SCHEMA': True,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
    },
    'ENUM_NAME_OVERRIDES': {},
    'TAG_SORTING': 'alpha',
    'EXTENSIONS_INFO': {
        'common.extensions.IsAuthenticatedExtension': {}
    }
}

# Internationalization
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", 'en-us')
TIME_ZONE = os.getenv("TIME_ZONE", 'Asia/Tehran')
USE_I18N = True
USE_TZ = True

# Static and Media files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



#redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

if REDIS_PASSWORD:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# settings.py
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
            # اختیاری:
            # "capacity": 1500,
            # "expiry": 10,
        },
    },
}


# Celery
CELERY_BROKER_URL = os.getenv("RABBITMQ_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TASK_ALWAYS_EAGER = False
CELERY_IMPORTS = ('core.tasks',)
# Celery Configuration Options
CELERY_TIMEZONE = os.getenv('TIME_ZONE')
CELERY_TASK_TRACK_STARTED = True

# MinIO
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = os.getenv("MINIO_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("MINIO_SECRET_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AUDITLOG_BUCKET = os.getenv("AUDITLOG_BUCKET", AWS_STORAGE_BUCKET_NAME)
AUDITLOG_PREFIX = os.getenv("AUDITLOG_PREFIX", "audit-logs")
AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
AWS_S3_REGION_NAME = "us-east-1"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_ADDRESSING_STYLE = "path"
AWS_DEFAULT_ACL = None


#----production
ENVIRONMENT = os.getenv("ENVIRONMENT")
# Allowed hosts
if ENVIRONMENT == "production":
    print(ENVIRONMENT)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    debug = False
    ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")
    ALLOWED_EXPORT_IPS = os.environ.get("ALLOWED_EXPORT_HOSTS", default='').split(",")
    CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", default='').split(",")
    ALLOWED_USER = os.environ.get("ALLOWED_USER", default='')
    SECRET_KEY_API = os.getenv("SECRET_KEY_API",default='')
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        # "http://37.32.15.242",
        # "https://37.32.15.242",
        # "http://localhost:3000",
        # "http://localhost:3001",
        # "http://localhost:3002",
    ]


else:  # development
    print(ENVIRONMENT)
    CORS_ALLOW_CREDENTIALS = True
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    ALLOWED_EXPORT_IPS = os.environ.get("ALLOWED_EXPORT_HOSTS", default='').split(",")
    ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")
    ALLOWED_USER = os.environ.get("ALLOWED_USER", default='')
    SECRET_KEY_API = os.getenv("SECRET_KEY_API", "fallback-secret-key")
    CORS_ALLOW_ALL_ORIGINS = False  # Explicitly disable
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:8000",  # FastAPI server
        "http://127.0.0.1:8000",
        # "http://37.32.15.242",
        # "https://37.32.15.242",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost",
        "http://localhost:8000",
        "http://127.0.0.1",
        "http://127.0.0.1:8000",
        # "http://37.32.15.242",
        # "https://37.32.15.242",
    ]


# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '__name__': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}



KAVENEGAR_API_KEY=os.environ.get("KAVENEGAR_API_KEY")