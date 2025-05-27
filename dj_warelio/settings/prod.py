import sys

sys.path.append('..')
from dj_warelio.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '0.0.0.0']

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': int(os.getenv("DB_PORT"))
    }
}
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"  # if you django verison is 4.2+ you should use this else you wont get the statuc files of panel admin
STATIC_URL = '/static/'
STATIC_ROOT = '/warelio/static'
'''
1- python manage.py migrate
2- python manage.py createsuperuser
3- python manage.py runserver
'''
