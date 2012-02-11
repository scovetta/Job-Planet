from os.path import abspath, dirname
from os import environ
from ConfigParser import RawConfigParser
import sys
import django
import glob

PROJECT_ROOT 	= dirname(dirname(abspath(__file__)))
SITE_ROOT 	= dirname(PROJECT_ROOT)
MEDIA_ROOT 	= SITE_ROOT + '/project/uploads'
TMP_DIR 	= SITE_ROOT + '/project/tmp'
LOCAL_SETTINGS 	= PROJECT_ROOT + '/settings/' + (environ.get('JOB_PLANET_ENV') or 'settings-development')

print "Site Root	%s" % SITE_ROOT
print "Project Root	%s" % PROJECT_ROOT
print "Local Settings	%s" % LOCAL_SETTINGS

config = RawConfigParser()
config.read( [ LOCAL_SETTINGS + '.ini', LOCAL_SETTINGS + '-private.ini' ] )

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1', '192.168.1.1')

ADMINS = (
     ('Michael Scovetta', 'michael.scovetta@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE':   config.get('database', 'DATABASE_ENGINE'),
        'NAME':     config.get('database', 'DATABASE_NAME'),
        'USER':     config.get('database', 'DATABASE_USER'),
        'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
        'HOST':     config.get('database', 'DATABASE_HOST'),
        'PORT':     config.get('database', 'DATABASE_PORT'),
    }
}

SITE_ID = 1

TIME_ZONE 	= 'America/New_York'
LANGUAGE_CODE 	= 'en-us'
USE_I18N 	= True
USE_L10N 	= True
APPEND_SLASH 	= True

MEDIA_URL 	= '/media/'
ADMIN_MEDIA_PREFIX = '/admin-static/'

SECRET_KEY 	= config.get('secrets', 'SECRET_KEY')
CSRF_MIDDLEWARE_SECRET = config.get('secrets', 'CSRF_MIDDLEWARE_SECRET')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django_notices.middleware.NoticeMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'grandcentral.lib.permission.PermissionRequiredMiddleware',
)

ROOT_URLCONF = 'grandcentral.urls'

TEMPLATE_DIRS = (
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    'django_notices.context_processors.notices',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.comments',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'secretballot',
    'south',
    'native_tags',
    'debug_toolbar',
    'gunicorn',
    'nexus',
    'gargoyle',
    'raven.contrib.django',
    'nexus_redis',
    'django_notices',
    'job.lib',
    'job.core',
)

# Automatically import applications
for d in glob.glob(PROJECT_ROOT + "/job/app_*"):
    d = d.replace(PROJECT_ROOT + '/job/', '')
    INSTALLED_APPS += ("job.%s" % d,)

if config.get('general', 'USE_CACHE') == 'True':
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': '127.0.0.1:6379',
            'OPTIONS': {
                'DB': 1,
            },
        },
    }
    NEXUS_REDIS_CONNECTIONS = [
        {'host': '127.0.0.1', 'port': 6379, 'db': 1},
    ]
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# Authentication
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

## static content ##
STATIC_URL = '/static/'

DJANGO_ADMIN_PATH = '/'.join((django.__file__).split('/')[:-1])

STATICFILES_DIRS = [
    DJANGO_ADMIN_PATH + '/contrib/admin/media',
    PROJECT_ROOT + '/static',
    SITE_ROOT + '/project/uploads',
]

STATIC_ROOT = SITE_ROOT + '/project/static'

# Messaging
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Web Server Errors
handler404 = 'core/error-404.tpl'
handler500 = 'core/error-500.tpl'

# Authentication
LOGIN_URL = '/auth/login'

# Logging
# Session Information
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = 'jpsid'

LOGGING = {
    'version' : 1,
    'disable_existing_loggers' : True,
    'formatters': {
        'verbose': {
            'format': config.get('log', 'LOG_FORMAT')
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter' : 'verbose',
            'filename' : SITE_ROOT + '/project/log/application.log',
            'maxBytes' : 1024*1024*10,
        }
        
    },
    'loggers': {
        'grandcentral' : {
            'handlers' : ['file'],
            'propagate' : True,
            'level' : 'DEBUG',
        },
        'django.request': {
            'handlers':['file'],
            'propagate': True,
            'level' : 'DEBUG',
        },
        'django_auth_ldap': {
            'handlers':['file'],
            'propagate': True,
            'level' : 'DEBUG',
        },
    }
}

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# Template filters & tags
DJANGO_BUILTIN_TAGS = (
    'native_tags.templatetags.native',
    'django.contrib.markup.templatetags.markup',
)

NATIVE_TAGS = (
    'native_tags.contrib.hash',
)

print "Completed import of settings.py"