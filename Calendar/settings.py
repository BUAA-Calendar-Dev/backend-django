import json
import os
from pathlib import Path

DEVELOP = False

# secret key
SECRET_KEY = "ThisIsOurDataBaseBackEnd"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

with open('setting.json', 'r', encoding='utf-8') as file:
    setting = json.load(file)
    IMG_SECRET_ID = setting['IMG_SECRET_ID']
    IMG_SECRET_KEY = setting['IMG_SECRET_KEY']
    IMG_BUCKET_NAME = setting['IMG_BUCKET_NAME']

    DB_NAME = setting['DB_NAME']
    DB_USER = setting['DB_USER']
    DB_PASSWORD = setting['DB_PASSWORD']
    DB_HOST = setting['DB_HOST']
    DB_PORT = setting['DB_PORT']

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "192.168.0.52",
    "127.0.0.1",
    "localhost"
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "Calendar",
    "application.activity",
    "application.classes",
    "application.message",
    "application.tag",
    "application.task",
    "application.users",
    "application.comment",
    "corsheaders",  # 注册 corsheaders
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 添加 CorsMiddleware
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Calendar.urls"

AUTH_USER_MODEL = 'users.User'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Calendar.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASE_DEVELOP = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DATABASE_GAUSS = {
    "default": {
        "ATOMIC_REQUESTS": True,
        "ENGINE": "django.db.backends.mysql",
        # 数据库名
        "NAME": DB_NAME,
        # 用户名
        "USER": DB_USER,
        # 密码
        "PASSWORD": DB_PASSWORD,
        # 数据库主节点IP
        "HOST": DB_HOST,
        # 端口
        "PORT": DB_PORT,
        "OPTIONS": {
            "init_command": "SET sql_mode = 'STRICT_TRANS_TABLES'"
        }
    }
}

DATABASES = DATABASE_DEVELOP if DEVELOP else DATABASE_GAUSS

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

APPEND_SLASH = False

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS configuration
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True  # 在开发环境中可以使用
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
]
CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:8000'
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
]

# 允许前端通过 cookie 发送和接收 session
SESSION_COOKIE_SAMESITE = None
CSRF_COOKIE_SAMESITE = None

# 确保 cookies 在跨域请求中被设置
SESSION_COOKIE_SECURE = False  # 在开发环境中可设置为 False，在生产环境中应设置为 True
CSRF_COOKIE_SECURE = False  # 在开发环境中可设置为 False，在生产环境中应设置为 True

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'  # 引擎
SESSION_COOKIE_NAME = "sessionid"  # Session的cookie保存在浏览器上时的key
SESSION_COOKIE_PATH = "/"  # Session的cookie保存的路径(默认)
SESSION_COOKIE_DOMAIN = None  # Session的cookie保存的域名(默认)
SESSION_COOKIE_SECURE = False  # 是否Https传输cookie
SESSION_COOKIE_HTTPONLY = True  # 是否Session的cookie只支持http传输(默认)
SESSION_COOKIE_AGE = 1209600  # Session的cookie失效日期(2周)(默认)
SESSION_SAVE_EVERY_REQUEST = False  # 是否设置关闭浏览器使得Session过期
SESSION_COOKIE_AT_BROWSER_CLOSE = False  # 是否每次请求都保存Session，默认修改之后才能保存
