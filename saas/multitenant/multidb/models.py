from django.db.backends.signals import connection_created
from django.db import connections
from django.db import models

from saas.multitenant.models import TenantDatabase as Database

from saas.multitenant.base.signals import *
from signals import *


def connection_debug(sender, connection, **kwargs):
    for key, conn in connections._connections.items():
        if conn == connection:
            print 'Connected to %s' % key


if getattr(settings, 'SAAS_MULTIDB_STARTUP', True): connection_created.connect(startup_db, dispatch_uid='db_autoload')
if getattr(settings, 'SAAS_MULTIDB_AUTOCREATE', True): models.signals.post_save.connect(create_db, sender=Database)
if getattr(settings, 'SAAS_MULTIDB_AUTODROP', True): models.signals.post_delete.connect(drop_db, sender=Database)
if getattr(settings, 'SAAS_MULTIDB_AUTOUNLOAD', True): models.signals.post_delete.connect(unload_db, sender=Database)
if settings.DEBUG: connection_created.connect(connection_debug)
