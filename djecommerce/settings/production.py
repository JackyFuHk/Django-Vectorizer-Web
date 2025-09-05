from .base import *

DEBUG = config('DEBUG', cast=bool)
ALLOWED_HOSTS = ['*'] 
DOMAIN_NAME=''
MIDDLEWARE += [ 'allauth.account.middleware.AccountMiddleware']
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]
ROOT_URLCONF = 'djecommerce.urls'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STRIPE_PUBLIC_KEY = config('STRIPE_LIVE_PUBLIC_KEY')
STRIPE_SECRET_KEY = config('STRIPE_LIVE_SECRET_KEY')
SECURE_SSL_REDIRECT  = True

CACHES = {  
    'default': {  
        'BACKEND': 'django_redis.cache.RedisCache',  
        'LOCATION': 'redis://127.0.0.1:6379/1',  # Redis 
        'OPTIONS': {  
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',  
            'CONNECTION_POOL_KWARGS': {'max_connections': 100},  
        },  
    },  
}