from django.core.management import call_command
from django.db import models
from django.conf import settings
from django.db.backends import signals

from south.models import MigrationHistory
from south.management.commands import syncdb

from appschema import schema
from appschema.models import Schema


def set_schema(*args, **kwargs):
    schema.schema_store.set_schema(schema.schema_store.current_schema())

def schema_created(sender, instance, created=False, **kwargs):
    if created:
        schema.create(instance.name)

def syncdb_schema(sender, instance, created=False, **kwargs):
    if created:
        call_command('syncdb', interactive=False, hostname=instance.public_name)
        
def migrate_schema(sender, instance, created=False, **kwargs):
    if created:
        try:
            migration = MigrationHistory.objects.latest('applied')
            try:
                call_command('migrate', migration.app_name, migration.migration, verbosity=0, hostname=instance.public_name)
            except Exception, err:
                call_command('migrate', migration.app_name, migration.migration, verbosity=0, hostname=instance.public_name)
        except MigrationHistory.DoesNotExist:
            call_command('migrate', verbosity=0, hostname=instance.public_name)

  
def schema_deleted(sender, instance, *args, **kwargs):
    schema.drop(instance.name)




def connect():
    signals.connection_created.connect(set_schema)
    
    models.signals.post_save.connect(schema_created, sender=Schema)
    models.signals.post_save.connect(syncdb_schema, sender=Schema)
    models.signals.post_save.connect(migrate_schema, sender=Schema)
    
    models.signals.post_delete.connect(schema_deleted, sender=Schema)
