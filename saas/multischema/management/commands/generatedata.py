from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings
from appschema.models import Schema
try:
    from dilla.management.commands import run_dilla
except ImportError, err:
    print 'Dilla not found.  (Hint: you need to be running development settings)'
    raise err
    
class Command(run_dilla.Command):
    option_list = run_dilla.Command.option_list + (
        make_option('--hostname', action='store', dest='hostname', default=None, help='Hostname of schema to use'),
        make_option('--schema', action='store', dest='schemaname', default=None, help='Nominates a specific schema to load fixtures into'),
        make_option('--all', action='store_true', dest='allschemas', default=False, help='Performs run_dilla on all schemas'),
    )
    help = run_dilla.Command.help + '\nWith schema supprt'
    
    def handle(self, *fixtures, **options):
        schemaname = options.get('schemaname', None)
        hostname = options.get('hostname', None)
        allschemas = options.get('allschemas', False)
        schemas = None
        
        if allschemas or schemaname or hostname:
            schemas = Schema.objects.active()
            if hostname:
                schemas = schemas.filter(public_name=hostname)
            if schemaname:
                schemas = schemas.filter(name=schemaname)
        
        if schemas:
            for schema in schemas:
                with schema:
                    super(Command, self).handle(*fixtures, **options)
        else:
            return super(Command, self).handle(*fixtures, **options)
