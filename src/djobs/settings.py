import os
import sys

from django.utils.crypto import get_random_string

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.environ.get('DJOBS_DATA_DIR', os.path.join(BASE_DIR, 'data'))
LOG_DIR = os.path.join(DATA_DIR, 'logs')
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static.dist')

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
if not os.path.exists(MEDIA_ROOT):
    os.mkdir(MEDIA_ROOT)

SECRET_FILE = os.path.join(DATA_DIR, '.secret')
if os.path.exists(SECRET_FILE):
    with open(SECRET_FILE, 'r') as f:
        SECRET_KEY = f.read().strip()
else:
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    SECRET_KEY = get_random_string(50, chars)
    with open(SECRET_FILE, 'w') as f:
        os.chmod(SECRET_FILE, 0o600)
        try:
            os.chown(SECRET_FILE, os.getuid(), os.getgid())
        except AttributeError:
            pass  # os.chown is not available on Windows
        f.write(SECRET_KEY)

debug_default = 'runserver' in sys.argv
DEBUG = os.environ.get('DJOBS_DEBUG', str(debug_default)) == 'True'

MAIL_FROM = SERVER_EMAIL = DEFAULT_FROM_EMAIL = os.environ.get('DJOBS_MAIL_FROM', 'admin@localhost')
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_HOST = os.environ.get('DJOBS_MAIL_HOST', 'localhost')
    EMAIL_PORT = int(os.environ.get('DJOBS_MAIL_PORT', '25'))
    EMAIL_HOST_USER = os.environ.get('DJOBS_MAIL_USER', '')
    EMAIL_HOST_PASSOWRD = os.environ.get('DJOBS_MAIL_PASSWORD', '')
    EMAIL_USE_TLS = os.environ.get('DJOBS_MAIL_TLS', 'False') == 'True'
    EMAIL_USE_SSL = os.environ.get('DJOBS_MAIL_SSL', 'False') == 'True'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + os.getenv('DJOBS_DB_TYPE', 'sqlite3'),
        'NAME': os.getenv('DJOBS_DB_NAME', 'db.sqlite3'),
        'USER': os.getenv('DJOBS_DB_USER', ''),
        'PASSWORD': os.getenv('DJOBS_DB_PASS', ''),
        'HOST': os.getenv('DJOBS_DB_HOST', ''),
        'PORT': os.getenv('DJOBS_DB_PORT', ''),
        'CONN_MAX_AGE': 0,
    }
}

SITE_URL = os.getenv('DJOBS_SITE_URL', 'http://localhost')
if SITE_URL == 'http://localhost':
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = [urlparse(SITE_URL).netloc]

if os.getenv('DJOBS_COOKIE_DOMAIN', ''):
    SESSION_COOKIE_DOMAIN = os.getenv('DJOBS_COOKIE_DOMAIN', '')
    CSRF_COOKIE_DOMAIN = os.getenv('DJOBS_COOKIE_DOMAIN', '')

SESSION_COOKIE_SECURE = os.getenv('DJOBS_HTTPS', 'True' if SITE_URL.startswith('https:') else 'False') == 'True'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djobs.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djobs.urls'

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

WSGI_APPLICATION = 'djobs.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/jobs/static/'
MEDIA_URL = '/jobs/media/'
