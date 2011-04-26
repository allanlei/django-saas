# -*- coding: utf-8 -*-
#
# This file is part of Django appschema released under the MIT license.
# See the LICENSE for more information.
from django.utils.datastructures import SortedDict
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_syncdb
from django.db.models.loading import cache
from django.conf import settings

try:
    from south.exceptions import NoMigrations
    from south.migration import Migrations
    south_ok = True
except ImportError:
    south_ok = False

from appschema.models import Schema



class RunWithApps(object):
    def __init__(self, apps):
        self.apps = apps
        
    def __enter__(self):
        self.installed_old = settings.INSTALLED_APPS
        self.app_store_old = cache.app_store
        
        settings.INSTALLED_APPS = self.apps
        cache.app_store = SortedDict([(key, value) for key, value in cache.app_store.items() if get_app_label(key) in self.apps])
    
    def __exit__(self, *args, **kwargs):
        if hasattr(self, 'installed_old'):
            settings.INSTALLED_APPS = self.installed_old
            del self.installed_old
        if hasattr(self, 'app_store_old'):
            cache.app_store = self.app_store_old
            del self.app_store_old


def get_app_label(app):
    """ Returns app label as Django make it. """
    return '.'.join( app.__name__.split('.')[0:-1])
    
def get_schemas(hostname=None, schemaname=None, allschemas=False):
    schemas = []
    if hostname is not None:
        schemas = [Schema.objects.active().get(public_name=hostname)]
    elif schemaname is not None:
        schemas = [Schema.objects.active().get(name=schemaname)]
    elif allschemas:
        schemas = Schema.objects.active()
    return schemas
    
def get_public_apps(appName=None, restricted=[None]):
    installed_apps = list(settings.INSTALLED_APPS)
    apps = []

    if hasattr(settings, 'APPSCHEMA_PUBLIC_APPS'):
        apps = list(settings.APPSCHEMA_PUBLIC_APPS)
    elif hasattr(settings, 'APPSCHEMA_PUBLIC_APPS_EXCLUDES'):
        apps = installed_apps
        restricted += list(settings.APPSCHEMA_PUBLIC_APPS_EXCLUDES)
    elif appName:
        apps = [appName]
    else:
        apps = installed_apps
    apps = [app for app in apps if app not in restricted]
    return apps
    
def get_isolated_apps(appName=None, restricted=[None, 'appschema']):
    installed_apps = list(settings.INSTALLED_APPS)
    apps = []
    
    if hasattr(settings, 'APPSCHEMA_ISOLATED_APPS'):
        apps = list(settings.APPSCHEMA_ISOLATED_APPS)
    elif hasattr(settings, 'APPSCHEMA_ISOLATED_APPS_EXCLUDES'):
        apps = installed_apps
        restricted += list(settings.APPSCHEMA_ISOLATED_APPS_EXCLUDES)
    elif appName:
        apps = [appName]
    else:
        apps = installed_apps
    apps = [app for app in apps if app not in restricted]
    return apps

def migratable(app):
    try:
        if south_ok:
            Migrations(app)
            return True
    except (NoMigrations, ImproperlyConfigured):
        pass
    return False
