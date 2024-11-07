"""
Django settings for AIPL_WEB_ERP project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os.path  
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'agratasinfotech.com', 'www.agratasinfotech.com']

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'AIPL',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AIPL_WEB_ERP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "AIPL" / "FrontEnd" / "Templates"], 
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


# # Ensure SecurityMiddleware is at the top of the MIDDLEWARE list
MIDDLEWARE.insert(0, 'django.middleware.security.SecurityMiddleware')

# # Security settings
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevents browsers from MIME-sniffing files
SECURE_BROWSER_XSS_FILTER = True    # Enables XSS filtering by the browser

# Enforce HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year; adjust based on preference
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# # Clickjacking protection
X_FRAME_OPTIONS = 'DENY'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# SMTP configuration for erp@agratasinfotech.com
EMAIL_HOST = 'mail.agratasinfotech.com'  # The SMTP server from your screenshot
EMAIL_PORT = 465  # Use port 465 for SSL
EMAIL_USE_SSL = True  # SSL for secure connection
EMAIL_HOST_USER = 'erp@agratasinfotech.com'  # Your new email
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')  # Replace with the actual password
DEFAULT_FROM_EMAIL = 'erp@agratasinfotech.com'  # The default 'From' email

# Set EMAIL_USE_TLS = False since you're using SSL (port 465)
EMAIL_USE_TLS = False


WSGI_APPLICATION = 'AIPL_WEB_ERP.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': os.getenv('DB_NAME'), # agratasi_agratasinfotech
		'USER': os.getenv('DB_USER'), # agratasi_root
		'PASSWORD': os.getenv('DB_PASSWORD'), # agratas9069076975
		'HOST':'localhost',
		'PORT':'3306',
	}
}
import os
BASE_DIR = Path(__file__).resolve().parent.parent

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',  # Logs only error and above level messages
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_error.log'),  # Log file path
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',  # Capture only errors and critical logs
            'propagate': True,
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# production setting to handle the staticfiles
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'AIPL' / 'FrontEnd' / 'static',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
# STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



JAZZMIN_SETTINGS = {
    "site_title": "AIPL Admin",
    "site_header": "AIPL Admin",
    "welcome_sign": "Welcome to Agratas Infotech Private Limited",
    "site_brand": "AIPL",
    
    # Sidebar Custom Links
    "custom_links": {
        "AIPL": [  # App name here
            {
                "name": "Analytics",
                "url": "analytics",  # URL name defined in urls.py
                "icon": "fas fa-chart-line",
                "permissions": ["AIPL.view_managetask"],  # Optional: restrict to staff with specific permissions
            },
        ]
    },
    
    # Customize appearance
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Analytics", "url": "analytics", "icon": "fas fa-chart-line"},
    ],

    # Footer customizations
    "copyright": "Agratas Infotech Private Limited © 2024",
}




