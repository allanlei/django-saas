from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.management.commands import loaddata

from appschema.models import Schema

class Command(loaddata.Command):
    option_list = loaddata.Command.option_list + (
        make_option('--hostname', action='store', dest='hostname', default=None, help='Hostname of schema to use'),
        make_option('--schema', action='store', dest='schemaname', default=None, help='Nominates a specific schema to load fixtures into'),
        make_option('--all', action='store_true', dest='allschemas', default=False, help='Performs loaddata on all schemas'),
    )
    help = loaddata.Command.help + ' with schema supprt'
    
    def handle(self, *fixtures, **options):
        schemaname = options.get('schemaname', None)
        hostname = options.get('hostname', None)
        allschemas = options.get('allschemas', False)
        schemas = []
        
        if allschemas or schemaname or hostname:
            schemas = Schema.objects.active()
            if hostname:
                schemas = schemas.filter(public_name=hostname)
            if schemaname:
                schemas = schemas.filter(name=schemaname)
                
        for schema in schemas:
            with schema:
                super(Command, self).handle(*fixtures, **options)
