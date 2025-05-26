import sys

sys.path.append('..')
from dj_warelio.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-xl#-%@z_jcf7itq$@8p-!r+=k5rm^6_gt2!_f6oxn^zmu*3d$h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

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

'''
1- python manage.py migrate
2- python manage.py createsuperuser
3- python manage.py runserver
'''