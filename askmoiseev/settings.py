"""
Django settings for askmoiseev project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ADMIN_MEDIA_PREFIX = '/admin/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'guvi_=wvvbu9+s%e6=qf(z&1)(!+jn#x&(hd6b=206=)hra_24'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

#add template dir
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]



ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ask',
    'loginsys',
    'custom_app',
    'widget_tweaks',
    'djangosphinx',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'askmoiseev.urls'

WSGI_APPLICATION = 'askmoiseev.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ask_db',
	'USER': 'askmoiseev',
	'PASSWORD': 'drovosek',
	'HOST': '',
	'PORT': '',	
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/'

STATiCFILES_DIRS = (
	('static', '/home/max/askmoiseev/static'),
)

MEDIA_ROOT = '/home/max/askmoiseev/uploads/'
MEDIA_URL = '/uploads/'


AUTH_USER_MODEL = 'loginsys.User'
AUTHENTICATION_BACKENDS = [
    'loginsys.UserBackend',
]


#SMTP
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_HOST_USER = 'streambuf@mail.ru'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'streambuf@mail.ru'
SERVER_EMAIL = 'streambuf@mail.ru'


from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    "custom_app.context_processors.top_tags_users",
)


SPHINX_PORT = 9845
SPHINX_SERVER = '127.0.0.1'
