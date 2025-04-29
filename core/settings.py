# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True) 
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='S#perS3crEt_007')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# Assets Management
ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets') 

# load production server from .env
ALLOWED_HOSTS        = ['*']
# Application definition

CSRF_TRUSTED_ORIGINS = [
    'http://quiz.chlosta.live',
    'https://quiz.chlosta.live',
]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'apps.authentication',
    'rest_framework',
    'rest_framework.authtoken',
    'landing',
    'apps.home',  # Enable the inner home (home)
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    "apps.home.middleware.LoginRequiredMiddleware",  # Add your custom middleware here
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "app/subject-list"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.context_processors.cfg_assets_root',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

#bellow is defauld database with sqlite3
if os.environ.get('DB_ENGINE') and os.environ.get('DB_ENGINE') == "postgresql":
    # Postgresql database
    DATABASES = { 
      'default': {
        'ENGINE'  : 'django.db.backends.postgresql', 
        'NAME'    : os.getenv('DB_NAME'     , 'p24_db'),
        'USER'    : os.getenv('DB_USERNAME' , 'p24_db_usr'),
        'PASSWORD': os.getenv('DB_PASS'     , 'p24_db_pwd'),
        'HOST'    : os.getenv('DB_HOST'     , 'postgres'),
        'PORT'    : os.getenv('DB_PORT'     , 5432),
        }, 
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)


#############################################################
#############################################################

AUTH_USER_MODEL = 'home.CustomUser'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# django-allauth settings
ACCOUNT_LOGIN_METHODS = {"email", "username"}  # Allow login with email or username
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]  # Required fields during signup
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # Enforce email verification
ACCOUNT_EMAIL_REQUIRED = True  # Email is required
ACCOUNT_USERNAME_REQUIRED = True  # Username is required
ACCOUNT_SIGNUP_REDIRECT_URL = '/'  # Redirect after signup
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/login/'  # Redirect after email confirmation for logged-in users
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/login/'  # Redirect after email confirmation for anonymous users
ACCOUNT_LOGOUT_REDIRECT_URL = '/login/'  # Redirect after logout

# Email backend configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.your-server.de'  # Replace with your SMTP server
EMAIL_PORT = 587  # Typically 587 for TLS
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')  # Your email address (set in .env file)
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')  # Your email password (set in .env file)
DEFAULT_FROM_EMAIL = 'QuizApp <noreply@chlosta.live>'  # Replace with your app's email

# settings.py

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')