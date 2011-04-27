from django.core.management import call_command
from django.conf import settings
import django.dispatch


db_route_read = django.dispatch.Signal(providing_args=[])
db_route_write = django.dispatch.Signal(providing_args=[])


db_pre_load = django.dispatch.Signal(providing_args=['instance'])
db_post_load = django.dispatch.Signal(providing_args=['instance'])

db_pre_unload = django.dispatch.Signal(providing_args=['instance'])
db_post_unload = django.dispatch.Signal(providing_args=['instance'])

def create_db(sender, instance, created=False, **kwargs):
    if created:
        db = instance
        if getattr(settings, 'SAAS_MULTIDB_GET_OR_CREATE', False):
            pass
        else:
            call_command('createdb', db.db, engine=db.engine, username=db.user, host=db.host, port=db.port, verbosity=0)
        if getattr(settings, 'SAAS_MULTIDB_AUTOLOAD', True):
            db.load()
        if getattr(settings, 'SAAS_MULTIDB_AUTOSYNC', True):
            call_command('syncdb', database=db.db, verbosity=0, noinput=True)

def drop_db(sender, instance, **kwargs):
    db = instance
    if getattr(settings, 'SAAS_MULTIDB_AUTOUNLOAD', True):
        db.unload()
#       call_command('dropdb', verbosity=0)
