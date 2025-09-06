from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-91b@&!&w_q%fxr6%6-u%g7a25rthl7_x5a*h1-fr=3&93t8wro'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', 'freshersguide.in']


# Application definition

INSTALLED_APPS = [
    'freshersapp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://freshersguide.in",
    "https://freshersguide.in",
]

ROOT_URLCONF = 'freshers_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(BASE_DIR / "freshers_frontend" / "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'freshers_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [BASE_DIR / "freshers_frontend" / "static"]


# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"  
# EMAIL_PORT = 587                
# EMAIL_USE_TLS = True         
# EMAIL_HOST_USER = "aaronmity2006@gmail.com"   
# EMAIL_HOST_PASSWORD = "ulkb uuhh qxxt vuuz" 
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

AUTH_USER_MODEL = "freshersapp.CustomUser"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = "aaronmity2006@gmail.com"

EMAIL_ACCOUNTS = [
    # {
    #     "EMAIL_HOST": "smtp.gmail.com",
    #     "EMAIL_PORT": 587,
    #     "EMAIL_HOST_USER": "aaronmity2006@gmail.com",
    #     "EMAIL_HOST_PASSWORD": "ulkb uuhh qxxt vuuz", 
    # },
    # {
    #     "EMAIL_HOST": "smtp.gmail.com",
    #     "EMAIL_PORT": 587,
    #     "EMAIL_HOST_USER": "astrodim006@gmail.com",
    #     "EMAIL_HOST_PASSWORD": "dmnp hudq jtnt moro",
    # },
    # {
    #     "EMAIL_HOST": "smtp.gmail.com",
    #     "EMAIL_PORT": 587,
    #     "EMAIL_HOST_USER": "freshers20iiv@gmail.com",
    #     "EMAIL_HOST_PASSWORD": "tpqw jtlc ksge udwv",
    # },
    # {
    #     "EMAIL_HOST": "smtp.gmail.com",
    #     "EMAIL_PORT": 587,
    #     "EMAIL_HOST_USER": "freshnit2k25@gmail.com",
    #     "EMAIL_HOST_PASSWORD": "jngp zwgn wrlt yika",
    # },
    # {
    #     "EMAIL_HOST": "smtp.gmail.com",
    #     "EMAIL_PORT": 587,
    #     "EMAIL_HOST_USER": "freshersnitpyk@gmail.com",
    #     "EMAIL_HOST_PASSWORD": "cbvz xnlc cndt yrzl ",
    # },
    #  {
    #     "EMAIL_HOST": "smtp.gmail.com",
    #     "EMAIL_PORT": 587,
    #     "EMAIL_HOST_USER": "freshers2knitpy@gmail.com",
    #     "EMAIL_HOST_PASSWORD": "ucta hukc shhl hepg",
    # },
    # {
    #     "EMAIL_HOST": "smtp.gmail.com",
    #     "EMAIL_PORT": 587,
    #     "EMAIL_HOST_USER": "freshers1styear@gmail.com",
    #     "EMAIL_HOST_PASSWORD": "gnnw ypup xbal oyiv",
    # },
    # {
    #     "EMAIL_HOST": "smtp.gmail.com",
    #     "EMAIL_PORT": 587,
    #     "EMAIL_HOST_USER": "freshersjuniors2k25@gmail.com",
    #     "EMAIL_HOST_PASSWORD": "esuw olee qvgg pnpv",
    # },
 
    # {
    #     "EMAIL_HOST": "smtp.gmail.com",
    #     "EMAIL_PORT": 587,
    #     "EMAIL_HOST_USER": "jnrfreshers2k25@gmail.com",
    #     "EMAIL_HOST_PASSWORD": "cjal mghh akse ecfc",
    # },
    # {
    #     "EMAIL_HOST": "smtp.gmail.com",
    #     "EMAIL_PORT": 587,
    #     "EMAIL_HOST_USER": "qubidim707@gmail.com",
    #     "EMAIL_HOST_PASSWORD": "eiqr bfav tymq qjyr",
    # },
    {
        "EMAIL_HOST": "smtp.gmail.com",
        "EMAIL_PORT": 587,
        "EMAIL_HOST_USER": "freshers2k25111@gmail.com",
        "EMAIL_HOST_PASSWORD": "gjgb yftn vjxw gkhw", 
    },
    {
        "EMAIL_HOST": "smtp.gmail.com",
        "EMAIL_PORT": 587,
        "EMAIL_HOST_USER": "freshers2k25222@gmail.com",
        "EMAIL_HOST_PASSWORD": "nzjc thdw lduf fpmj",
    },
    {
        "EMAIL_HOST": "smtp.gmail.com",
        "EMAIL_PORT": 587,
        "EMAIL_HOST_USER": "freshers2k25333@gmail.com",
        "EMAIL_HOST_PASSWORD": "uxfr htev gmcy uxne",
    },
    
]
