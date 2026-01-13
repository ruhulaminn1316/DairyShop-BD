"""
Django settings for ec project.
"""

from pathlib import Path
from django.contrib.messages import constants as messages
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'sharatacharjee6@gmail.com'
EMAIL_HOST_PASSWORD = 'iyxrzfhdjoxvguhq'  # ⚠️ no spaces
DEFAULT_FROM_EMAIL = 'Daily Dairy Shop <sharatacharjee6@gmail.com>'




# ---------------- BASE DIR ----------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------- SECURITY ----------------
SECRET_KEY = 'django-insecure-4^hblj$3@q-n3mp%vmvy&367_c*@jqj$bo7@25wq_6mkd9gu&f'
DEBUG = True

ALLOWED_HOSTS = [
    'dailydairyshop-3.onrender.com',
    '127.0.0.1',
    'localhost'
]

# ---------------- LOGIN ----------------
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ---------------- MESSAGE TAGS ----------------
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# ---------------- INSTALLED APPS ----------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',   # ✅ REQUIRED

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
   


    # your apps
    'app',
    'adminpanel',

    # cloudinary
    'cloudinary',
    'cloudinary_storage',
]

SITE_ID = 1

# ---------------- AUTHENTICATION ----------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

# ---------------- GOOGLE OAUTH ----------------
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}

# ---------------- CLOUDINARY ----------------
cloudinary.config(
    cloud_name="dfkzni71h",
    api_key="813172256721514",
    api_secret="bip7IZdpeaHp9w71Up-HncjPoX0",
    secure=True
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ---------------- MIDDLEWARE ----------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # ✅ THIS LINE FIXES YOUR ERROR
    'allauth.account.middleware.AccountMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



# ---------------- URL / TEMPLATE ----------------
ROOT_URLCONF = 'ec.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'app' / 'templates'],
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

WSGI_APPLICATION = 'ec.wsgi.application'

# ---------------- DATABASE ----------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------- PASSWORD VALIDATORS ----------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------- I18N ----------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------- STATIC ----------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------- PAYMENT ----------------
BKASH_APP_KEY = os.environ.get('BKASH_APP_KEY', '')
BKASH_APP_SECRET = os.environ.get('BKASH_APP_SECRET', '')
BKASH_BASE_URL = os.environ.get('BKASH_BASE_URL', 'https://tokenized-sandbox.bkash.com')

NAGAD_MERCHANT_ID = os.environ.get('NAGAD_MERCHANT_ID', '')
NAGAD_MERCHANT_PASS = os.environ.get('NAGAD_MERCHANT_PASS', '')
NAGAD_BASE_URL = os.environ.get('NAGAD_BASE_URL', 'https://sandbox.mynagad.com')

