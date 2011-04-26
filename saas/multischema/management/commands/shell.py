from optparse import make_option
from django.core.management.commands import shell

from appschema.schema import schema_store
from appschema.models import Schema


class Command(shell.Command):
    option_list = shell.Command.option_list + (
        make_option('--schema', action='store', dest='schemaName', default=None, help='Schema to use'),
        make_option('--hostname', action='store', dest='hostname', default=None, help='Hostname of schema to use'),
    )
    help = shell.Command.help + '\t(Overrided with schema switching)'
    
    def handle(self, schemaName=None, hostname=None, *args, **kwargs):
        schema = None
        if hostname:
            schema = Schema.objects.active().get(public_name=hostname)
        elif schemaName:
            schema = Schema.objects.active().get(name=schemaName)
        
        if schema:
            with schema:
                return super(Command, self).handle(*args, **kwargs)
        else:
            return super(Command, self).handle(*args, **kwargs)
