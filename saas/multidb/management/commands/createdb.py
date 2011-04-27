# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connection

from optparse import make_option
import subprocess

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--engine', action='store', dest='engine', default=settings.DATABASES['default']['ENGINE'], help='Database engine'),
        make_option('--username', action='store', dest='username', default=settings.DATABASES['default']['USER'], help='Database username'),
        make_option('--host', action='store', dest='host', default=settings.DATABASES['default']['HOST'], help='Database host'),
        make_option('--port', action='store', dest='port', default=settings.DATABASES['default']['PORT'], help='Database port'),
    )
    help = 'Creates a new empty database to be used with syncdb. SQLite3 does not need to be created as syncdb will create it'
    
    def handle(self, name, **options):
        engine = options['engine']
        username = options['username']
        hostname = options['host']
        port = options['port']
        if engine == 'django.db.backends.postgresql_psycopg2':
            #hostname:port:database:username:password in ~/.pgpass
            return self.create_postgresql_psycopg2(name, username=username, hostname=hostname, port=port)
        elif engine == 'django.db.backends.sqlite3':
            return self.create_sqlite3(name)
        elif engine == 'django.db.backends.postgresql':
            return self.create_postgresql(name)
        elif engine == 'django.db.backends.mysql':
            return self.create_mysql(name)
        elif engine == 'django.db.backends.oracle':
            return self.create_oracle(name)
    
    def run_command(self, cmd):
        try:
            return subprocess.check_call(cmd)
        except subprocess.CalledProcessError, ex:
            return ex.returncode
            
    def create_postgresql_psycopg2(self, name, username=None, hostname=None, port=5432):
        cmd = ['createdb']
        if username: cmd.append('--username=%s' % username)
        if hostname: cmd.append('--hostname=%s' % hostname)
        if port: cmd.append('--port=%s' % port)
        cmd.append(name)
        return self.run_command(cmd)
    
    def create_sqlite3(self, name):
        return self.run_command(['touch', name])
    
    def create_postgresql(self, name):
        raise NotImplementedError
    
    def create_mysql(self, name):
        raise NotImplementedError
    
    def create_oracle(self, name):
        raise NotImplementedError
