"""

        
Django settings for saturn project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
# Brennan Williams!!!! Matt Corbett!!!!! Spencer Harrison!!!!! Stetson Kent!!!!
# 6 December 2021

# IS INTEX PROJECT!!!!


from pathlib import Path
import os
import dj_database_url 
import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', 'https://tutorstudentproject.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'titan.apps.TitanConfig',
    'whitenoise.runserver_nostatic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

ROOT_URLCONF = 'saturn.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'saturn.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': 'tutor',
#     'USER': 'postgres',
#     'PASSWORD': 'Happ1n3ss',
#     'HOST': 'localhost',
#     'PORT' : 5432,
#     'DISABLE_SERVER_SIDE_CURSORS': True
#     }
# } 
# DATABASES = {
#     'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': 'tutor',
#     'USER': 'postgres',
#     'PASSWORD': 'Luke1Luke1',
#     'HOST': 'localhost',
#     'PORT' : 5432,
#     'DISABLE_SERVER_SIDE_CURSORS': True
#     }
# } 
# DATABASES = {
#     'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': 'intex',
#     'USER': 'postgres',
#     'PASSWORD': 'mcorbet3',
#     'HOST': 'localhost',
#     'PORT' : 5432,
#     'DISABLE_SERVER_SIDE_CURSORS': True
#     }
# } 


# DATABASES = {
#     'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': 'tutor',
#     'USER': 'postgres',
#     'PASSWORD': 'admin',
#     'HOST': 'localhost',
#     'PORT' : 5434,
#     'DISABLE_SERVER_SIDE_CURSORS': True
#     }
# } 


DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'tutor',
    'USER': 'myadmin',
    'PASSWORD': 'my@dmin1',
    'HOST': 'is415mcorbet3.postgres.database.azure.com',
    'PORT' : 5432,
    'DISABLE_SERVER_SIDE_CURSORS': True
    }
} 
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env) 
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'saturn/static')
]     
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = 'test@test.com'

django_heroku.settings(locals())