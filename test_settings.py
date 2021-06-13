from pathlib import Path
from miq.config import (
    AUTH_USER_MODEL,
)

# AUTH_USER_MODEL = 'miq.User'
# TEMPLATES_DIR = 'templates'
# TEMPLATES_DIR = BASE_DIR / 'templates'
BASE_DIR = Path(__file__).resolve().parent

SITE_ID = 1
API_PATH = 'api/v1'
SECRET_KEY = 'test-key'
DEBUG = True
CORS_ORIGIN = 'http://127.0.0.1:3000'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #
    'django.contrib.sites',
    'django.contrib.sitemaps',
    #
    'rest_framework',
    'miq.apps.MiqConfig',
]

ROOT_URLCONF = 'tests.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
    'other': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': env('DB_NAME'),
#         'USER': env('DB_USER'),
#         'PASSWORD': env('DB_PWD'),
#         'HOST': '',
#         'PORT': '',
#     }
# }

MIDDLEWARE = [
    # CORS
    'miq.middleware.CORSMiddleware',
    #
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        # 'DIRS': [TEMPLATES_DIR],
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Set for all views
    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 16,
}
