# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connection

from optparse import make_option


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--username', action='store', dest='username', default='', help='Database username'),
        make_option('--password', action='store', dest='password', default='', help='Database password'),
        make_option('--host', action='store', dest='host', default='', help='Database host'),
        make_option('--port', action='store', dest='port', default='', help='Database port'),
    )
    help = 'Creates a new empty database'
    
    def handle(self, name, engine, **options):
        if engine == 'django.db.backends.postgresql_psycopg2':
            self.create_postgresql_psycopg2(name, **options)
    
    def create_postgresql_psycopg2(self, name, **options):
        isolation_level = connection.isolation_level
        connection.isolation_level = 0
        cursor = connection.cursor()
        cursor.execute('CREATE DATABASE %s', [name])
        connection.isolation_level = isolation_level
    
    
    from django.db import connection, transaction
    cursor = connection.cursor()

    # Data modifying operation - commit required
    cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
    transaction.commit_unless_managed()

    # Data retrieval operation - no commit required
    cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
    row = cursor.fetchone()

    return row
    
    
#        connection = DatabaseWrapper({
#            'DATABASE_HOST': settings.DATABASE_HOST,
#            'DATABASE_NAME': settings.DATABASE_NAME + '_test',
#            'DATABASE_OPTIONS': settings.DATABASE_OPTIONS,
#            'DATABASE_PASSWORD': settings.DATABASE_PASSWORD,
#            'DATABASE_PORT': settings.DATABASE_PORT,
#            'DATABASE_USER': settings.DATABASE_USER,
#            'TIME_ZONE': settings.TIME_ZONE,
#        })
#        connection.creation.create_test_db(verbosity, autoclobber=not interactive)
        
        
        
        
        
        
        
#from django.db.backends.postgresql_psycopg2.base import DatabaseWrapper
#from django.db import connection

#class FlexDatabaseCreation(DatabaseCreation):
#    def create_test_db(self, verbosity=1, autoclobber=False):
#        ...
#        self.connection.settings_dict["DATABASE_NAME"] = test_database_name
#        connection.settings_dict["DATABASE_NAME"] = test_database_name # New code.
#        ...
#        self.connection.settings_dict["DATABASE_SUPPORTS_TRANSACTIONS"] = can_rollback
#        connection.settings_dict["DATABASE_SUPPORTS_TRANSACTIONS"] = can_rollback # New code.
#        
#class FlexDatabaseWrapper(DatabaseWrapper):
#    def __init__(self, *args, **kwargs):
#        super(FlexDatabaseWrapper, self).__init__(*args, **kwargs)
#        self.creation = FlexDatabaseCreation(self)
