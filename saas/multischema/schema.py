# -*- coding: utf-8 -*-
#
# This file is part of Django appschema released under the MIT license.
# See the LICENSE for more information.

from django.conf import settings
from django.db import connection, models, transaction
from threading import local

__all__ = ('schema_store',)

class SchemaStore(local):
    """
    A simple thread safe store that will set search_path when asked for.
    """
    def __init__(self):
        self.clear()
    
    def current_schema(self, check=False):
        if check:
            cursor = connection.cursor()
            cursor.execute('SHOW search_path')
            row = cursor.fetchone()
            paths = [path.replace('"', '').strip() for path in row[0].split(',')]
            return paths[0]
        return self._schema
        
    def clear(self):
        self._schema = None
    
    def reset_path(self, cursor=None):
        self.clear()
        self.set_schema(cursor=cursor)
    
    @transaction.commit_on_success
    def set_schema(self, schema=None, force=False, cursor=None):
        cursor = cursor or connection.cursor()
        paths = []
        if schema is not None:
            paths.append(schema)
        if not force:
            paths += list(getattr(settings, 'APPSCHEMA_DEFAULT_PATH', ['public']))
        cursor.execute('SET search_path = %s;' % ','.join(['%s'] * len(paths)), paths)
        transaction.set_dirty()
        
schema_store = SchemaStore()

def escape_schema_name(name):
    """ Escape system names for PostgreSQL. Should do the trick. """
    return name.replace('"', '""')

@transaction.commit_on_success
def create(name):
    cursor = connection.cursor()
    cursor.execute('CREATE SCHEMA "%s"' % escape_schema_name(name))
    transaction.set_dirty()

@transaction.commit_on_success
def drop(name, silent=True):
    cursor = connection.cursor()
    cursor.execute('DROP SCHEMA %s "%s" CASCADE' % ('IF EXISTS' if silent else '', escape_schema_name(name)))
    transaction.set_dirty()
