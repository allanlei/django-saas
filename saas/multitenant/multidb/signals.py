from django.core.management import call_command
from django.conf import settings


def create_db(sender, instance, created=False, **kwargs):
    if created:
        db = instance
        if getattr(settings, 'SAAS_MULTIDB_GET_OR_CREATE', False):
            pass
        else:
            call_command('createdb', db.db, engine=db.engine, username=db.user, host=db.host, port=db.port, verbosity=0)
        if getattr(settings, 'SAAS_MULTIDB_AUTOLOAD', True):
            db.load()
        if getattr(settings, 'SAAS_MULTIDB_AUTOSYNC', True) and db.is_loaded():
            call_command('syncdb', database=db.db, verbosity=0, interactive=False)
    
def drop_db(sender, instance, **kwargs):
    db = instance
    db.unload()
    call_command('dropdb', db.name, engine=db.engine, username=db.user, host=db.host, port=db.port, verbosity=0)

def unload_db(sender, instance, **kwargs):
    instance.unload()

from django.db.backends.signals import connection_created
def startup_db(sender, connection, signal=None, **kwargs):
    from models import Database
    Database.objects.using('default').all().load()          #Problem with initial syncdb
    connection_created.disconnect(dispatch_uid='db_autoload')
    print 'LOADED'
