# -*- coding: utf-8 -*-
#
# This file is part of Django appschema released under the MIT license.
# See the LICENSE for more information.
from django.db import models, connection, transaction
from django.core.management import call_command
from django.conf import settings

from appschema.managers import SchemaManager
from appschema.schema import schema_store
from appschema import schema

from datetime import datetime


class Schema(models.Model):
    created = models.DateTimeField(default=datetime.now)    #models.DateTimeField(auto_now_add=True)
#    accessed = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64)
    public_name = models.CharField(max_length=255, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    
    objects = SchemaManager()
    
    class Meta:
        unique_together = ('name', 'public_name')
    
    def is_syncdb_required(self):
        return True
    
    def is_migrate_required(self):
        return False
    
    @transaction.commit_on_success
    def rename(self, name):
        cursor = connection.cursor()
        cursor.execute('ALTER SCHEMA "%s" RENAME TO "%s"' % (self.name, name), [])
        transaction.set_dirty()
        self.name = name
        self.save()
        
    def exists(self):
        cursor = connection.cursor()
        cursor.execute("SELECT schemata.schema_name FROM information_schema.schemata WHERE schemata.schema_name = %s;", [self.name])
        row = cursor.fetchone()
        return row is not None
        
    def enter(self):
        self._schema_temp = schema_store.current_schema()
        schema_store.set_schema(schema=self.name, force=True)
        if settings.DEBUG: print ' ** Using database with schema "%s" **' % self
    
    def exit(self):     #Needs fixing. Doesn't actually get current schema. Possibly do the same as Site framework
        if hasattr(self, '_schema_temp'):
            if getattr(settings, 'APPSCHEMA_RESET_PATH', True):
                schema_store.set_schema(schema=self._schema_temp or 'public', force=True)
                if settings.DEBUG: print '\n ** Restoring database to schema "%s" **' % (self._schema_temp or 'public', )
            del self._schema_temp
        
    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.public_name)
    
    def __enter__(self):
        self.enter()
        return self
    
    def __exit__(self, *args, **kwargs):
        self.exit()


from signals import connect
connect()
