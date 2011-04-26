from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.management.commands import dumpdata

from appschema.models import Schema
from appschema import utils

class Command(dumpdata.Command):
    option_list = dumpdata.Command.option_list + (
        make_option('--hostname', action='store', dest='hostname', default=None, help='Hostname of schema to use'),
        make_option('--schema', action='store', dest='schemaname', default=None, help='Nominates a specific schema to load fixtures into'),
        make_option('--pg_dump', action='store', dest='pg_dump', default=False, help='Dump as pg_dump'),
    )
    help = dumpdata.Command.help + ' with schema supprt'
    
    def handle(self, *args, **options):
        schemaname = options.pop('schemaname') if 'schemaname' in options else None
        hostname = options.pop('hostname') if 'hostname' in options else None
        pg_dump = options.pop('pg_dump') if 'pg_dump' in options else False
        
        filters = {}
        if schemaname:
            filters['name'] = schemaname
        elif hostname:
            filters['public_name'] = hostname

        options['exclude'] = options['exclude'] + utils.get_public_apps()
        for schema in Schema.objects.active().filter(**filters):
            with schema:
                if pg_dump:
                    pass
                else:
                    print super(Command, self).handle(*args, **options)
                    print
