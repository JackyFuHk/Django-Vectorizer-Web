import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = config('SECRET_KEY')
APPEND_SLASH = True
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth',  
    'rest_auth.registration', 
    'crispy_forms',
    'django_countries',

    
    'core',


]
SESSION_ENGINE = 'django.contrib.sessions.backends.db' 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djecommerce.wsgi.application'

# Static files (CSS, JavaScript, Images)
DOMAIN_NAME= config('DOMAIN_NAME')
STATIC_URL = config('STATIC_URL')
MEDIA_URL = config('MEDIA_URL')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')

# Auth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'social.backends.weixin.WeixinOAuth2'
)

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

# CRISPY FORMS
HANDLER404 = 'core.views.custom_404_view'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGGING = {  
    'version': 1,  
    'disable_existing_loggers': False,  
    'handlers': {  
        'file': {  
            'level': 'ERROR',  # 或者 'DEBUG' 以记录所有日志  
            'class': 'logging.FileHandler',  
            'filename': './log/debug.log',  # 日志文件的路径  
        },  
        'console': {  
            'level': 'ERROR',  # 控制台输出的日志级别  
            'class': 'logging.StreamHandler',  
        },  
    },  
    'loggers': {  
        'django': {  
            'handlers': ['file', 'console'],  # 指定要使用的处理器  
            'level': 'ERROR',  # Django 框架的日志级别  
            'propagate': True,  # 是否将日志消息传播到父记录器  
        },  
        'core': {  # 替换为您的应用名  
            'handlers': ['file', 'console'],  
            'level': 'DEBUG',  # 您应用的日志级别，可以设置为 'DEBUG' 以捕获更多信息  
            'propagate': False,  # 通常不需要将日志传播到父记录器，特别是当您已经指定了处理器时  
        },  
        'core': {  # 替换为您的应用名  
            'handlers': ['file', 'console'],  
            'level': 'INFO',  # 您应用的日志级别，可以设置为 'DEBUG' 以捕获更多信息  
            'propagate': False,  # 通常不需要将日志传播到父记录器，特别是当您已经指定了处理器时  
        },  
    },  
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
ACCOUNT_EMAIL_VERIFICATION = 'optional'


SOCIAL_AUTH_WEIXIN_KEY  = config('SOCIAL_AUTH_WEIXIN_KEY')
SOCIAL_AUTH_WEIXIN_SECRET  = config('SOCIAL_AUTH_WEIXIN_SECRET')
WECHAT_REDIRECT_URI = config('WECHAT_REDIRECT_URI')
WECHAT_MSG_TOKEN = config('WECHAT_MSG_TOKEN')

SMS_ACCESS_ID = config('SMS_ACCESS_ID')
SMS_ACCESS_SECRET = config('SMS_ACCESS_SECRET')


# 国际化 中英双语
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True
    
USE_TZ = True
    
LANGUAGES = (
    ('en', 'English'),
    ('zh-hans', '中文简体'),
)
LOCALE_PATHS = (
        os.path.join(BASE_DIR, 'locale'),
    )



WECHAT_PAY_APP_ID = config('WECHAT_PAY_APP_ID')
WECHAT_PAY_MCH_ID = config('WECHAT_PAY_MCH_ID')
WECHAT_PAY_API_KEY = config('WECHAT_PAY_API_KEY')
WECHAT_PAY_NOTIFY_URL = config('WECHAT_PAY_NOTIFY_URL')
trade_type = 'NATIVE'
UFDODER_URL = config('UFDODER_URL')
CREATE_IP = config('CREATE_IP')
QRCODEPATH = "static/qrcode"