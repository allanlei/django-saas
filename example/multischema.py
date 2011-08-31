from settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tenancy',                      # Or path to database file if using sqlite3.
        'USER': 'tenancy',                      # Not used with sqlite3.
        'PASSWORD': 'tenancy',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

INSTALLED_APPS += (
    'tenancy.schema',
)

MIDDLEWARE_CLASSES = tuple((
    'tenancy.middleware.SignalTenantMiddleware',
) + MIDDLEWARE_CLASSES)

DATABASE_ROUTERS += ['app.routers.SignalMultiSchemaTenantRouter']


SAAS_TENANCY_MODEL = None
#SAAS_TENANCY_PRIVATE = None
#SAAS_TENANCY_PUBLIC = None
SAAS_TENANCY_FN = lambda request: request.get_host().replace('.test.com', '')

