import os
from distutils.util import strtobool

from django.contrib.messages import constants as messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _, gettext_noop
from dotenv import load_dotenv
from pathlib import Path

########################################
# BASE SETTINGS
########################################
load_dotenv()
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent
SITE_ID = 1
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
ROOT_URLCONF = 'TownhouseWorldRealestate.urls'
WSGI_APPLICATION = 'TownhouseWorldRealestate.wsgi.application'


########################################
# APPS
########################################
# Application definition
MODULES = [
    'FunctionModule.accounts.apps.AccountsConfig',
    'FunctionModule.pages.apps.PagesConfig',
    'FunctionModule.listings.apps.ListingsConfig',
    'FunctionModule.transactions.apps.TransactionsConfig',
    'FunctionModule.realtors.apps.RealtorsConfig',
    'FunctionModule.customers.apps.CustomersConfig',
    'FunctionModule.cadastral.apps.CadastralConfig',
    'FunctionModule.blog.apps.BlogConfig',
    'FunctionModule.zalo.apps.ZaloConfig',
    'FunctionModule.hitcount.apps.HitcountConfig',
]
THIRD_PARTIES = [
    'allauth',
    'location_field',
    'ajax_select',
    'rolepermissions',
    'debug_toolbar',
    'rest_framework',
    #'corsheaders',
    'django_filters',
    'adminplus',
    'cachalot',
    'crispy_forms',
    'pwa',
    #'django_gulp',
    'import_export',
    ]
BUILT_IN_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.postgres',
    'django.contrib.sitemaps',
]
INSTALLED_APPS = BUILT_IN_APPS + THIRD_PARTIES + MODULES

########################################
# MIDDLEWARE
########################################
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

########################################
# TEMPLATES
########################################
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

########################################
# DATABASE
########################################
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
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


########################################
# STATIC SETTINGS (CSS, JavaScript, Images)
########################################
STATIC_ROOT = os.path.join(BASE_DIR, 'compiled_staticfiles')
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# Media Folder Settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'
AVATAR_PHOTO_URL = 'photos/avatar/'


########################################
# AUTHENTICATION
########################################
AUTH_USER_MODEL = 'accounts.User'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
if ENVIRONMENT == 'production':
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_FORMS = {'signup': 'accounts.forms.CustomUserCreationForm'}
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""
#LOGIN_REDIRECT_URL = reverse_lazy("admin:index")
#LOGIN_URL = reverse_lazy("accounts_login")
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

########################################
# EMAIL
########################################
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = '***' #my gmail password
EMAIL_HOST_USER = 'thegioinhaphovietnam@gmail.com' #my gmail username
DEFAULT_FROM_EMAIL = 'thegioinhaphovietnam@gmail.com'
SERVER_EMAIL = 'thegioinhaphovietnam@gmail.com'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


########################################
# INTERNATIONALISATION
########################################
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
#USE_L10N = True
USE_TZ = True
APPEND_SLASH = False
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale/'),)
COMPRESS_OFFLINE = True

LANGUAGES = [
    ('vi', gettext_noop('Vietnamese')),
    ('en-us', gettext_noop('English')),
]
LANGUAGES_BIDI = ["vi", "en-us", "ur"]
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = None
LANGUAGE_COOKIE_DOMAIN = None
LANGUAGE_COOKIE_PATH = '/'
LANGUAGE_COOKIE_SECURE = False
LANGUAGE_COOKIE_HTTPONLY = False
LANGUAGE_COOKIE_SAMESITE = None
DATE_FORMAT = ( ( '%d/%m/%Y' ))
DATE_INPUT_FORMATS = ( ('%d/%m/%Y'),)
DATETIME_FORMAT = (( 'd/m/Y H:i' ))
DATETIME_INPUT_FORMATS = (('%d/%m/%Y %H:%i'),)


########################################
# SECURITY
########################################
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'w6rm%l&xim0ivll-li$u6fg8)6k8-$7uar^f#33ht5sutw8e!#')
DEBUG = bool(os.getenv("DJANGO_DEBUG", "False").lower() in ["true", "1"])
#DEBUG = strtobool(os.getenv('DEBUG', 'True'))
DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True
ALLOWED_HOSTS = []
CORS_ALLOWED_ORIGINS = [
        'https://thegioinhaphovietnam.com.vn',
        'http://localhost:8888',
    ]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGIN_REGEXES = [
    'https://thegioinhaphovietnam.com.vn',
    'http://localhost:8888',
    ]
CSRF_TRUSTED_ORIGINS = [
        'https://thegioinhaphovietnam.com.vn',
        'http://localhost:8888',
    ]

########################################
# SITE SETTINGS
########################################
# todo: set your site name, your country and your support email here
SITE_NAME = "TGNP"
SITE_LOCATION = "Việt Nam"
#SUPPORT_EMAIL = "support@thegioinhaphovietnam.com"

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'danger'
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


########################################
# CACHES
########################################
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 15  # 15M
FILE_UPLOAD_MAX_MEMORY_SIZE = DATA_UPLOAD_MAX_MEMORY_SIZE
DATA_UPLOAD_MAX_NUMBER_FIELDS = 4000  # higher than the count of fields
CACHES = {
    'default': {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        'LOCATION': os.getenv('REDIS_URL', default='redis://redis:6379')
    }
}
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SECURE = True


########################################
# APPLICATION ADDON
########################################
#GDAL_LIBRARY_PATH = r'C:\OSGeo4W'
#GEOS_LIBRARY_PATH = r'build\lib.win-amd64-3.9\osgeo'
if os.name == 'nt':
    import platform
    OSGEO4W = r"C:\OSGeo4W"
    #if '64' in platform.architecture()[0]:
    #    OSGEO4W += "64"
    assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W
    os.environ['OSGEO4W_ROOT'] = OSGEO4W
    os.environ['GDAL_DATA'] = OSGEO4W + r"\apps\gdal"
    os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
    os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']

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

MEILI_MASTER_KEY = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'
MEILI_HOST = os.getenv('MEILI_HOST', 'search_engine')
MEILI_PORT = os.getenv('MEILI_PORT', 7700)

# SESSION_SAVE_EVERY_REQUEST = True
HITCOUNT_KEEP_HIT_ACTIVE = {'minutes': 60}
HITCOUNT_HITS_PER_IP_LIMIT = 0  # unlimited
HITCOUNT_EXCLUDE_USER_GROUP = ()  # not used
HITCOUNT_KEEP_HIT_IN_DATABASE = {'seconds': 10}

ZALO_APP_ID = '4421936851919043973'
ZALO_APP_SECRET = '2QuDKw9NrSy8g5n2O3MI'
ZALO_APP_CALLBACK_URL = '/accounts/social/login-zalo-callback'
ZALO_CODE_CHALLENGE = 'MTQ4OTkyQkE1NTUwQjBDM0EwNjIwRTczNjc1NUIzRjBFMzIwMjUwOTkzOUNBMERCREQ5NzNBMzMyQkY4RThFMA=='
ZALO_STATE = 'yes'
ZALO_ACCESS_TOKEN = 'DSz52EH7GbSnnaaAwqvELZp4IGtiKqObJgah2zj9SpuCXICMcaXvBIYm0WYH958e0jShCQu-Mm9wwoyKzpbq5oNAFHsyGdKG6P47Dva5I6mquo0veXSk1YdzNX-eTWr3CVb5LvOO50r3cHW5-X9V8Ntb9NNpE4fFNUuWH8TYQMyHYZf1nqDtTMA226hO3KnYK_enMUCwG6P4qaffboOGCZ7tJpM1VJ8eCBm-49P2Opink0u4epb7EWtgAHgz5sG-DTis5ES8J21quJS8-szzK5oV3LJU4Lv9KUaX5UEvFcpYM4zG'
ZALO_REFRESH_TOKEN = '5Mp9Y3PSGMWfUflF5ZXjS3bEWAHRS6T4La_5a0Lb4q4KPOkIEqPfHoquf-0vUKiqNqgcx2TFQ098QhZOMcOZ2NDF-9rSA0So6rtRtMbJ3pbcRlpN3qiW1Xn7ZCK85dDG3q6Bp1GLx4fc53EVjIPoC-yrbjhjKNvkr0MogVuc4s__0kN2XKeJH-m2XhppDJ1mX5x1jK-9xMHBTIrX'