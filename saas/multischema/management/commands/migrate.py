# -*- coding: utf-8 -*-
#
# This file is part of Django appschema released under the MIT license.
# See the LICENSE for more information.
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

from south.management.commands import migrate
from south.models import MigrationHistory

from appschema.models import Schema
from appschema.schema import schema_store
from appschema.utils import get_public_apps, get_isolated_apps, get_schemas, RunWithApps, migratable

from optparse import make_option

class Command(migrate.Command):
    option_list = migrate.Command.option_list + (
        make_option('--hostname', action='store', dest='hostname', default=None, help='Hostname of schema to use'),
        make_option('--schema', action='store', dest='schemaname', default=None, help='Nominates a specific schema to load fixtures into'),
        make_option('--allschemas', action='store_true', dest='allschemas', default=True, help='Performs run_dilla on all schemas'),
    )
    help = migrate.Command.help + '\nWith schema supprt'
    
    def logging(self, message):
        if self.debug and settings.DEBUG:
            print message

    def handle(self, *args, **options):
        self.debug = bool(options.get('verbosity', 0))
        hostname = options.pop('hostname')
        schemaname = options.pop('schemaname')
        allschemas = options.pop('allschemas')
        
        args = list(args)
        appName = args[0] if len(args) > 0 else None
        public_apps = [app for app in get_public_apps(appName=appName) if migratable(app)]
        
        if (hostname is None and schemaname is None) and len(public_apps):
            self.logging('Migrating "master" for %d apps:' % len(public_apps))
            schema_store.reset_path()
            for app in public_apps:
                self.logging('\t- ' + app)
                if len(args) > 0:
                    args[0] = app
                else:
                    args.append(app)
                super(Command, self).handle(*args, **options)
        
        schemas = get_schemas(hostname=hostname, schemaname=schemaname, allschemas=allschemas)
        isolated_apps = [app for app in get_isolated_apps(appName=appName) if migratable(app)]
        
        for schema in schemas:
            self.logging('\n')
            with schema:
                self.logging('Migrating "%s" for %d apps:' % (schema, len(isolated_apps)))
                for app in isolated_apps:
                    with RunWithApps([app]):
                        if len(args) > 0:
                            args[0] = app
                        else:
                            args.append(app)
                    
                        super(Command, self).handle(*args, **options)
                        self.logging('\t- %s (Migrated)' % app)
                        
        if hostname is None and schemaname is None and len(schemas):
            migrations = []
            with schemas[0]:
                for migration in MigrationHistory.objects.all():
                    migrations.append(migration)
            MigrationHistory.objects.all().delete()
            for migration in migrations:
                migration.save()
