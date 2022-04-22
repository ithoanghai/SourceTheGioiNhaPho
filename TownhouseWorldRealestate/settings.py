"""
Django settings for TownhouseWorldRealestate project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from distutils.util import strtobool

from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _, gettext_noop
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'w6rm%l&xim0ivll-li$u6fg8)6k8-$7uar^f#33ht5sutw8e!#')

DEBUG = strtobool(os.getenv('DEBUG', 'true'))
DEBUG_PROPAGATE_EXCEPTIONS = True

SITE_ID = 1

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

ALLOWED_HOSTS = ['*']

# Application definition
MODULES = [
    'FunctionModule.accounts.apps.AccountsConfig',
    'FunctionModule.pages.apps.PagesConfig',
    'FunctionModule.listings.apps.ListingsConfig',
    'FunctionModule.transactions.apps.TransactionsConfig',
    'FunctionModule.realtors.apps.RealtorsConfig',
    'FunctionModule.customers.apps.CustomersConfig',
    'FunctionModule.cadastral.apps.CadastralConfig',
]

THIRD_PARTIES = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'location_field.apps.DefaultConfig',
    'ajax_select',
    'rolepermissions',
    'debug_toolbar',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'adminplus',
    'cachalot',
]

BUILT_IN_APPS = [
    # 'admin_numeric_filter',
    # 'django.contrib.admin',
    'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.postgres',
]

INSTALLED_APPS = BUILT_IN_APPS + THIRD_PARTIES + MODULES

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'TownhouseWorldRealestate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'TownhouseWorldRealestate.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'tgnp'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

AUTH_USER_MODEL = 'accounts.User'

if ENVIRONMENT == 'production':
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

AUTHENTICATION_BACKENDS = [
    'FunctionModule.accounts.auth.RealEstateAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

LANGUAGE_CODE = 'vi'
LANGUAGES = [
    ('vi', gettext_noop('Vietnamese')),
    ('en-us', gettext_noop('English')),
]
LANGUAGES_BIDI = ["ar-dz", "fa", "ur"]

# Settings for language cookie
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = None
LANGUAGE_COOKIE_DOMAIN = None
LANGUAGE_COOKIE_PATH = '/'
LANGUAGE_COOKIE_SECURE = False
LANGUAGE_COOKIE_HTTPONLY = False
LANGUAGE_COOKIE_SAMESITE = None

COMPRESS_OFFLINE = True
COMPRESS_OFFLINE_CONTEXT = [
    {"LANGUAGE_BIDI": True},
]

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = False

USE_L10N = True

USE_TZ = True

APPEND_SLASH = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/deployment/
STATIC_ROOT = os.path.join(BASE_DIR, 'compiled_staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Media Folder Settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'danger'
}

GOOGLE_MAP_API_KEY = os.getenv('GOOGLE_MAP_API_KEY', '')
GEOEARTH_API_KEY = os.getenv('GEOEARTH_API_KEY', '')
MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY',
                           'pk.eyJ1Ijoia2llbm5ndXllbjExMDEiLCJhIjoiY2ttaHRqZTgzMGF0YzJ3bXVvYW9ncnh0ZiJ9.xar2mZcYZJ1qK4i2mRDa0Q')

LOCATION_FIELD = {
    'map.provider': 'google',
    'search.provider': 'nominatim',
    # 'provider.mapbox.access_token': 'pk.eyJ1Ijoia2llbm5ndXllbjExMDEiLCJhIjoiY2ttaHRqZTgzMGF0YzJ3bXVvYW9ncnh0ZiJ9.xar2mZcYZJ1qK4i2mRDa0Q',
    'provider.google.api_key': GOOGLE_MAP_API_KEY
}

INTERNAL_IPS = [
    '127.0.0.1',
    '172.17.0.1',
    '172.24.0.1',
    '*'
]

REST_FRAMEWORK = {
    'DEFAULT_MODEL_SERIALIZER_CLASS': (
        'rest_framework.serializers.HyperlinkedModelSerializer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
        #        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 1,
    'UNICODE_JSON': True,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 15  # 15M
FILE_UPLOAD_MAX_MEMORY_SIZE = DATA_UPLOAD_MAX_MEMORY_SIZE
DATA_UPLOAD_MAX_NUMBER_FIELDS = 4000  # higher than the count of fields

CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        'LOCATION': os.getenv('REDIS_URL', default='redis://redis:6379/1')
    }
}

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomUserCreationForm'
}
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SDK_URL': '//connect.facebook.net/vi_vn/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name'
        ],
        'EXCHANGE_TOKEN': True,
        'VERSION': 'v10.0',
    }
}
LOGIN_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

MEILI_MASTER_KEY = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
MEILI_HOST = os.getenv('MEILI_HOST', 'search_engine')
MEILI_PORT = os.getenv('MEILI_PORT', 7700)
